/**
 * Voice Assistant for RideShare Pro
 * Implements Web Speech API for hands-free operation
 * Supports Customer, Driver, and Admin voice commands
 */

class VoiceAssistant {
    constructor(role) {
        this.role = role; // 'customer', 'driver', or 'admin'
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.transcriptElement = null;
        this.statusElement = null;
        
        this.init();
    }

    init() {
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Speech recognition not supported');
            this.speak('Voice assistant is not supported in your browser');
            return;
        }

        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-IN'; // Indian English
        this.recognition.maxAlternatives = 1;

        // Event handlers
        this.recognition.onstart = () => this.onStart();
        this.recognition.onresult = (event) => this.onResult(event);
        this.recognition.onerror = (event) => this.onError(event);
        this.recognition.onend = () => this.onEnd();

        // Create UI elements
        this.createUI();
    }

    createUI() {
        // Voice transcript panel
        if (!document.getElementById('voiceTranscript')) {
            const transcript = document.createElement('div');
            transcript.id = 'voiceTranscript';
            transcript.className = 'voice-transcript';
            transcript.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4><i class="fas fa-microphone"></i> Voice Assistant</h4>
                    <button onclick="voiceAssistant.close()" style="background: none; border: none; cursor: pointer; font-size: 1.2rem;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="transcript-text" id="transcriptText">Click the microphone to speak</div>
                <div class="transcript-status" id="transcriptStatus">Ready</div>
            `;
            document.body.appendChild(transcript);
        }

        this.transcriptElement = document.getElementById('transcriptText');
        this.statusElement = document.getElementById('transcriptStatus');
    }

    start() {
        if (!this.recognition) {
            this.speak('Voice recognition is not available');
            return;
        }

        try {
            this.recognition.start();
            this.isListening = true;
            
            // Update UI
            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.classList.add('listening');
            }
            
            document.getElementById('voiceTranscript').classList.add('show');
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }

    stop() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
            
            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.classList.remove('listening');
            }
        }
    }

    close() {
        this.stop();
        document.getElementById('voiceTranscript').classList.remove('show');
    }

    onStart() {
        this.transcriptElement.textContent = 'Listening...';
        this.statusElement.textContent = 'Speak now';
    }

    onResult(event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        this.transcriptElement.textContent = interimTranscript || finalTranscript;

        if (finalTranscript) {
            this.processCommand(finalTranscript.toLowerCase().trim());
        }
    }

    onError(event) {
        console.error('Speech recognition error:', event.error);
        this.statusElement.textContent = `Error: ${event.error}`;
        
        if (event.error === 'no-speech') {
            this.speak('I didn\'t hear anything. Please try again.');
        } else if (event.error === 'not-allowed') {
            this.speak('Microphone access is required for voice commands.');
        }
    }

    onEnd() {
        this.isListening = false;
        const voiceBtn = document.getElementById('voiceBtn');
        if (voiceBtn) {
            voiceBtn.classList.remove('listening');
        }
        this.statusElement.textContent = 'Finished';
    }

    processCommand(command) {
        console.log(`Processing command: ${command}`);
        
        switch (this.role) {
            case 'customer':
                this.processCustomerCommand(command);
                break;
            case 'driver':
                this.processDriverCommand(command);
                break;
            case 'admin':
                this.processAdminCommand(command);
                break;
            default:
                this.speak('Unknown role');
        }
    }

    // Customer Commands
    processCustomerCommand(command) {
        // Book ride: "book ride from [location] to [location]"
        if (command.includes('book ride') || command.includes('book a ride')) {
            const fromMatch = command.match(/from\s+([a-z\s]+?)\s+to/);
            const toMatch = command.match(/to\s+([a-z\s]+?)(?:\s|$)/);
            
            if (fromMatch && toMatch) {
                const from = fromMatch[1].trim();
                const to = toMatch[1].trim();
                this.bookRide(from, to);
            } else {
                this.speak('Please specify both pickup and dropoff locations');
            }
        }
        // Show nearby vehicles
        else if (command.includes('show nearby') || command.includes('nearby vehicles')) {
            this.speak('Showing nearby available vehicles');
            if (typeof loadNearbyVehicles === 'function') {
                loadNearbyVehicles();
            }
        }
        // Cancel booking
        else if (command.includes('cancel')) {
            this.speak('Canceling your ride');
            if (document.getElementById('cancelBtn')) {
                document.getElementById('cancelBtn').click();
            }
        }
        // Help
        else if (command.includes('help')) {
            this.speak('You can say: Book ride from location to location, Show nearby vehicles, Cancel booking');
        }
        else {
            this.speak('I didn\'t understand that command. Say help for available commands.');
        }
    }

    // Driver Commands
    processDriverCommand(command) {
        // Accept ride
        if (command.includes('accept ride') || command.includes('accept')) {
            this.speak('Accepting the ride');
            const acceptBtn = document.querySelector('.accept-btn');
            if (acceptBtn) {
                acceptBtn.click();
            } else {
                this.speak('No pending ride to accept');
            }
        }
        // Reject ride
        else if (command.includes('reject ride') || command.includes('reject')) {
            this.speak('Rejecting the ride');
            const rejectBtn = document.querySelector('.reject-btn');
            if (rejectBtn) {
                rejectBtn.click();
            }
        }
        // Start trip
        else if (command.includes('start trip') || command.includes('start ride')) {
            this.speak('Starting the trip');
            const startBtn = document.getElementById('startRideBtn');
            if (startBtn) {
                startBtn.click();
            }
        }
        // Complete trip
        else if (command.includes('complete trip') || command.includes('complete ride')) {
            this.speak('Completing the trip');
            const completeBtn = document.getElementById('completeRideBtn');
            if (completeBtn) {
                completeBtn.click();
            }
        }
        // Go online/offline
        else if (command.includes('go online')) {
            this.speak('Going online');
            const toggle = document.getElementById('onlineToggle');
            if (toggle && !toggle.classList.contains('active')) {
                toggle.click();
            }
        }
        else if (command.includes('go offline')) {
            this.speak('Going offline');
            const toggle = document.getElementById('onlineToggle');
            if (toggle && toggle.classList.contains('active')) {
                toggle.click();
            }
        }
        // Help
        else if (command.includes('help')) {
            this.speak('You can say: Accept ride, Reject ride, Start trip, Complete trip, Go online, Go offline');
        }
        else {
            this.speak('I didn\'t understand that command. Say help for available commands.');
        }
    }

    // Admin Commands
    processAdminCommand(command) {
        // Track vehicle
        if (command.includes('track vehicle')) {
            const vehicleMatch = command.match(/track vehicle\s+([a-z0-9\-]+)/i);
            if (vehicleMatch) {
                const vehicleNumber = vehicleMatch[1].toUpperCase().replace(/\s+/g, '-');
                this.speak(`Tracking vehicle ${vehicleNumber}`);
                if (typeof trackVehicle === 'function') {
                    trackVehicle(vehicleNumber);
                }
            } else {
                this.speak('Please specify the vehicle number');
            }
        }
        // Show analytics
        else if (command.includes('show analytics') || command.includes('analytics')) {
            this.speak('Showing analytics dashboard');
            window.scrollTo({ top: document.querySelector('.analytics-grid').offsetTop, behavior: 'smooth' });
        }
        // Filter by city
        else if (command.includes('filter') && command.includes('bangalore')) {
            this.speak('Filtering by Bangalore');
            document.querySelector('[data-city="bangalore"]').click();
        }
        else if (command.includes('filter') && command.includes('porto')) {
            this.speak('Filtering by Porto');
            document.querySelector('[data-city="porto"]').click();
        }
        else if (command.includes('show all') || (command.includes('filter') && command.includes('all'))) {
            this.speak('Showing all cities');
            document.querySelector('[data-city="all"]').click();
        }
        // Refresh data
        else if (command.includes('refresh')) {
            this.speak('Refreshing dashboard data');
            if (typeof loadDashboardData === 'function') {
                loadDashboardData();
            }
            if (typeof updateMap === 'function') {
                updateMap();
            }
        }
        // Help
        else if (command.includes('help')) {
            this.speak('You can say: Track vehicle number, Show analytics, Filter Bangalore, Filter Porto, Show all, Refresh');
        }
        else {
            this.speak('I didn\'t understand that command. Say help for available commands.');
        }
    }

    // Helper function to book ride
    bookRide(from, to) {
        const pickupSelect = document.getElementById('pickupLocation');
        const dropoffSelect = document.getElementById('dropoffLocation');
        
        if (pickupSelect && dropoffSelect) {
            // Try to match locations
            const pickupOption = Array.from(pickupSelect.options).find(opt => 
                opt.text.toLowerCase().includes(from.toLowerCase())
            );
            const dropoffOption = Array.from(dropoffSelect.options).find(opt => 
                opt.text.toLowerCase().includes(to.toLowerCase())
            );
            
            if (pickupOption && dropoffOption) {
                pickupSelect.value = pickupOption.value;
                dropoffSelect.value = dropoffOption.value;
                
                // Trigger change events
                pickupSelect.dispatchEvent(new Event('change'));
                dropoffSelect.dispatchEvent(new Event('change'));
                
                this.speak(`Booking ride from ${pickupOption.text} to ${dropoffOption.text}`);
                
                setTimeout(() => {
                    const bookBtn = document.getElementById('bookBtn');
                    if (bookBtn && !bookBtn.disabled) {
                        bookBtn.click();
                    }
                }, 1000);
            } else {
                this.speak('Could not find those locations. Please try again.');
            }
        }
    }

    // Text-to-speech
    speak(text) {
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-IN';
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        this.synthesis.speak(utterance);
    }
}

// Global instance - will be initialized based on page role
let voiceAssistant;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Detect role from page
    let role = 'customer'; // default
    
    if (window.location.pathname.includes('driver')) {
        role = 'driver';
    } else if (window.location.pathname.includes('admin')) {
        role = 'admin';
    }
    
    // Create voice assistant instance
    voiceAssistant = new VoiceAssistant(role);
    
    // Attach to voice button
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', function() {
            if (voiceAssistant.isListening) {
                voiceAssistant.stop();
            } else {
                voiceAssistant.start();
            }
        });
    }
    
    console.log(`Voice assistant initialized for ${role} role`);
});
