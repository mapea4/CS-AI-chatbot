// --- DOM Elements ---
const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const sendIcon = document.getElementById('send-icon');
const loadingSpinner = document.getElementById('loading-spinner');
const welcomeContainer = document.getElementById('welcome-container');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const chatHistoryList = document.getElementById('chat-history-list');
const mainContent = document.getElementById('main-content');

// --- State Management ---
const USER_ID = JSON.parse(mainContent.dataset.userId || 'null');
const API_URL = mainContent.dataset.apiUrl;
const DEADLINES_URL = mainContent.dataset.deadlinesUrl;

let chatHistory = [];
let currentChatId = null;
const synth = window.speechSynthesis;

function prefixKey(key) {
    return `user_${USER_ID}_${key}`;
}

// --- Core Functions ---

window.onload = () => {
    loadChatHistoryList();
    const latestChatId = localStorage.getItem(prefixKey('latestChatId'));
    if (latestChatId) {
        loadConversation(latestChatId);
    } else {
        startNewChat();
    }
    // Add initial rows to GPA calculators (links to gpa_calculator.js)
    if (window.addGpaCourseRow) addGpaCourseRow();
    if (window.addGpaAssignmentRow) addGpaAssignmentRow();

    fetchUpcomingDeadlines();
};

async function fetchUpcomingDeadlines() {
    try {
        const response = await fetch(DEADLINES_URL);
        if (!response.ok) return; 
        
        const data = await response.json();
        const deadlines = data.deadlines;
        
        const container = document.getElementById('upcoming-deadlines-container');
        const list = document.getElementById('upcoming-deadlines-list');
        
        if (deadlines && deadlines.length > 0) {
            list.innerHTML = ''; 
            deadlines.forEach(line => {
                const li = document.createElement('li');
                li.innerHTML = line; 
                list.appendChild(li);
            });
            container.style.display = 'block'; 
        } else {
            container.style.display = 'none'; 
        }
    } catch (error) {
        console.error("Error fetching deadlines:", error);
        document.getElementById('upcoming-deadlines-container').style.display = 'none';
    }
}

function startNewChat() {
    chatWindow.innerHTML = ''; 
    chatWindow.appendChild(welcomeContainer); 
    welcomeContainer.classList.remove('hidden'); 
    
    fetchUpcomingDeadlines();
    
    chatHistory = []; 
    currentChatId = `chat_${new Date().getTime()}`; 
    saveConversation();
    
    // --- START: SIDEBAR FIX ---
    // Reload the list in the sidebar so the "New Chat" appears
    loadChatHistoryList();
    // Highlight the "New Chat" item in the sidebar
    setActiveChat(currentChatId);
    // --- END: SIDEBAR FIX ---
    
    if (window.innerWidth < 768) {
        toggleSidebar();
    }
    synth.cancel();
}

function loadConversation(chatId) {
    const storedHistory = localStorage.getItem(prefixKey(chatId));
    if (!storedHistory) {
        return startNewChat(); 
    }
    chatHistory = JSON.parse(storedHistory);
    currentChatId = chatId;
    
    chatWindow.innerHTML = '';
    if (chatHistory.length === 0) {
        chatWindow.appendChild(welcomeContainer); 
        welcomeContainer.classList.remove('hidden'); 
        fetchUpcomingDeadlines();
    } else {
        welcomeContainer.classList.add('hidden'); 
        chatHistory.forEach(msg => appendMessage(msg.role, msg.content));
    }

    setActiveChat(chatId);
    synth.cancel();
}

function saveConversation() {
    if (!currentChatId) return;
    localStorage.setItem(prefixKey(currentChatId), JSON.stringify(chatHistory));
    localStorage.setItem(prefixKey('latestChatId'), currentChatId); 
    updateChatListTitle(currentChatId);
}

function sendSuggestedPrompt(promptText) {
    chatInput.value = promptText;
    handleMessageSubmit(new Event('submit')); 
}

async function handleMessageSubmit(event) {
    event.preventDefault();
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    synth.cancel();
    
    welcomeContainer.classList.add('hidden'); 
    chatHistory.push({ role: 'user', content: userMessage });
    appendMessage('user', userMessage);
    chatInput.value = '';
    
    const thinkingIndicator = appendThinkingIndicator();
    toggleLoading(true);
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ history: chatHistory })
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 401) {
                throw new Error("Your session has expired. Please log out and log in again.");
            }
            throw new Error(errorData.error || "An unknown error occurred.");
        }

        const data = await response.json();
        const aiMessage = data.answer;
        
        thinkingIndicator.remove();
        chatHistory.push({ role: 'assistant', content: aiMessage });
        appendMessage('assistant', aiMessage);
        saveConversation();
        
    } catch (error) {
        if (thinkingIndicator) thinkingIndicator.remove();
        console.error("Error sending message:", error);
        appendMessage('assistant', `Sorry, I've run into an error: ${error.message}`);
    } finally {
        toggleLoading(false);
    }
}

// --- UI Helper Functions ---

function appendMessage(role, message) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('flex', 'flex-col', 'w-full'); 
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', 'p-3', 'rounded-lg', 'shadow-md');
    
    if (role === 'user') {
        messageDiv.classList.add('user-message');
        messageDiv.textContent = message;
        messageContainer.classList.add('items-end'); 
        messageContainer.appendChild(messageDiv);
    } else {
        messageDiv.classList.add('ai-message');
        messageContainer.classList.add('items-start'); 
        
        let sanitizedMessage = message.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        sanitizedMessage = sanitizedMessage.replace(/\*\*(.*?)\*\*/g, '$1'); 
        
        const markdownLinkRegex = /\[.*?\]\((https?:\/\/[^\s]+)\)/g;
        sanitizedMessage = sanitizedMessage.replace(markdownLinkRegex, '$1');
        const urlRegex = /(https?:\/\/[^\s]+[^\s.,!?()])/g;
        let linkifiedMessage = sanitizedMessage.replace(
            urlRegex, 
            '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-300 hover:underline">$1</a>'
        );

        const mapRegex = /(McMechen|Calloway|Hurt|Truth|Key|CARC|Engineering|Student Center)/gi;
        linkifiedMessage = linkifiedMessage.replace(
            mapRegex, 
            '<a href="https://map.morgan.edu/" target="_blank" title="Find on Map" class="text-blue-300 hover:underline">$1&nbsp;🗺️</a>'
        );

        messageDiv.innerHTML = linkifiedMessage.replace(/\n/g, '<br>');

        const speakButton = document.createElement('button');
        speakButton.classList.add('speak-button');
        speakButton.innerHTML = `
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="text-gray-700">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.114-1.631.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
            </svg>`;
        
        const textToSpeak = message.replace(/<[^>]*>?/gm, '').replace(/\n/g, ' ');
        speakButton.dataset.message = textToSpeak;
        speakButton.onclick = () => speakText(speakButton.dataset.message);
        
        messageContainer.appendChild(messageDiv);
        messageContainer.appendChild(speakButton);
    }
    
    chatWindow.appendChild(messageContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight; 
    return messageContainer;
}

function speakText(textToSpeak) {
    synth.cancel(); 
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    const voices = synth.getVoices();
    let femaleVoice = voices.find(voice => 
        voice.lang.includes('en') && (voice.name.includes('Female') || voice.name.includes('Zira') || voice.name.includes('Google US English'))
    );
    if (!femaleVoice) {
        femaleVoice = voices.find(voice => voice.lang.includes('en-US'));
    }
    utterance.voice = femaleVoice || voices[0];
    utterance.pitch = 1;
    utterance.rate = 1;
    synth.speak(utterance);
}

function appendThinkingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.id = "thinking-indicator"; 
    messageDiv.classList.add('chat-message', 'ai-message', 'p-3', 'rounded-lg', 'shadow-md', 'thinking-bubble');
    messageDiv.innerHTML = `<div class="dot"></div><div class="dot"></div><div class="dot"></div>`;
    const container = document.createElement('div');
    container.classList.add('flex', 'flex-col', 'items-start');
    container.appendChild(messageDiv);
    chatWindow.appendChild(container);
    chatWindow.scrollTop = chatWindow.scrollHeight; 
    return container;
}

function toggleLoading(isLoading) {
    if (isLoading) {
        sendIcon.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
        sendButton.disabled = true;
        chatInput.disabled = true;
    } else {
        sendIcon.classList.remove('hidden');
        loadingSpinner.classList.add('hidden');
        sendButton.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
    }
}

function toggleSidebar() {
    sidebar.classList.toggle('sidebar-open');
    sidebarOverlay.classList.toggle('hidden');
}

// --- Sidebar History Functions ---

function loadChatHistoryList() {
    chatHistoryList.innerHTML = ''; 
    const userPrefix = prefixKey('chat_'); 
    const chatIds = Object.keys(localStorage)
        .filter(key => key.startsWith(userPrefix))
        .sort((a, b) => {
            const timeA = a.split('_')[2] || 0;
            const timeB = b.split('_')[2] || 0;
            return timeB - timeA; 
        });
    
    chatIds.forEach(prefixedChatId => {
        const chatId = prefixedChatId.substring(prefixKey('').length);
        const history = JSON.parse(localStorage.getItem(prefixedChatId) || '[]');
        const title = getChatTitle(history);
        const li = document.createElement('li');
        li.id = `chat-item-${chatId}`; 
        li.innerHTML = `
            <div class="sidebar-link flex items-center justify-between group p-2 rounded-lg hover:bg-gray-700">
                <a href="#" id="chat-link-${chatId}" 
                   onclick="loadConversation('${chatId}')" 
                   class="flex-1 text-sm text-gray-200 truncate">
                    ${title}
                </a>
                <button onclick="deleteChat(event, '${chatId}')" 
                        class="text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity" 
                        title="Delete chat">
                    <svg width="16" height="16" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor">
                        <path d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;
        chatHistoryList.appendChild(li);
    });
}

function deleteChat(event, chatId) {
    event.stopPropagation(); 
    if (confirm('Are you sure you want to delete this chat?')) {
        localStorage.removeItem(prefixKey(chatId));
        const latestChatKey = prefixKey('latestChatId');
        if (localStorage.getItem(latestChatKey) === chatId) {
            localStorage.removeItem(latestChatKey);
        }
        
        // --- START: SIDEBAR FIX ---
        if (currentChatId === chatId) {
            // If they deleted the active chat, start a new one
            startNewChat();
        } else {
            // If they deleted a different chat, just remove it from the list
            loadChatHistoryList();
        }
        // --- END: SIDEBAR FIX ---
    }
}

function getChatTitle(history) {
    if (!history || history.length === 0) return "New Chat";
    const firstUserMessage = history.find(msg => msg.role === 'user');
    const title = firstUserMessage ? firstUserMessage.content : "New Chat";
    return title.length > 25 ? title.substring(0, 25) + "..." : title;
}

function updateChatListTitle(chatId) {
    const chatItem = document.getElementById(`chat-item-${chatId}`);
    if (chatItem) {
        const title = getChatTitle(chatHistory);
        const anchorTag = chatItem.querySelector('a');
        if (anchorTag) {
            anchorTag.textContent = title;
        }
    } else {
        loadChatHistoryList();
    }
}

function setActiveChat(chatId) {
    document.querySelectorAll('#chat-history-list div').forEach(div => {
        const anchor = div.querySelector('a');
        if (anchor && anchor.id === `chat-link-${chatId}`) {
            div.classList.add('bg-gray-700', 'sidebar-link-active'); 
        } else {
            div.classList.remove('bg-gray-700', 'sidebar-link-active');
        }
    });
}

chatForm.addEventListener('submit', handleMessageSubmit);