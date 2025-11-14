document.addEventListener('DOMContentLoaded', () => {
    // Initialize the application
    const trendBtn = document.getElementById('trend-btn');
    const generateBtn = document.getElementById('generate-btn');

    if (trendBtn) {
        trendBtn.addEventListener('click', runTrendAnalysis);
    }
    if (generateBtn) {
        generateBtn.addEventListener('click', generateDesign);
    }
});

async function runTrendAnalysis() {
    const resultsContainer = document.getElementById('trend-results');
    const statusMessage = document.getElementById('trend-status');
    const promptsList = document.getElementById('prompts-list');

    // Show loading state
    statusMessage.textContent = '🔍 Analyzing market trends... This may take a moment.';
    statusMessage.className = 'status-message';
    resultsContainer.innerHTML = '';
    promptsList.innerHTML = '';

    try {
        const response = await fetch('/api/run-trend-analysis', { method: 'POST' });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Clear status and display trends and prompts
        statusMessage.textContent = '✅ Analysis complete. Here are the latest trends:';
        displayTrends(data.trends);
        displayPrompts(data.prompts);

    } catch (error) {
        statusMessage.textContent = `❌ Trend analysis failed: ${error.message}`;
        statusMessage.className = 'status-message error';
        console.error('Trend analysis failed:', error);
    }
}

function displayTrends(trends) {
    const resultsContainer = document.getElementById('trend-results');
    resultsContainer.innerHTML = ''; // Clear previous results

    trends.forEach(trend => {
        const trendCard = document.createElement('div');
        trendCard.className = 'trend-card';

        const trendImage = document.createElement('img');
        trendImage.src = trend.image_url;
        trendImage.alt = trend.title;

        const trendAnalysis = document.createElement('p');
        trendAnalysis.textContent = trend.analysis;

        trendCard.appendChild(trendImage);
        trendCard.appendChild(trendAnalysis);
        resultsContainer.appendChild(trendCard);
    });
}

function displayPrompts(prompts) {
    const promptsList = document.getElementById('prompts-list');
    promptsList.innerHTML = ''; // Clear previous prompts

    prompts.forEach(prompt => {
        const listItem = document.createElement('li');
        listItem.textContent = prompt;
        listItem.onclick = () => {
            document.getElementById('design-prompt').value = prompt;
        };
        promptsList.appendChild(listItem);
    });
}

async function generateDesign() {
    const prompt = document.getElementById('design-prompt').value.trim();
    const modelId = document.getElementById('design-model').value;
    const resultsContainer = document.getElementById('design-results');
    const statusMessage = document.getElementById('status-message');

    if (!prompt) {
        alert('Please select a prompt or write your own!');
        return;
    }

    // Show loading state
    resultsContainer.innerHTML = '';
    statusMessage.textContent = '🎨 Generating your t-shirt design... Please wait.';
    statusMessage.className = 'status-message';

    try {
        const options = { model: modelId, quality: 'hd' };
        const imageElement = await puter.ai.txt2img(prompt, options);

        // Style the generated image and add download functionality
        imageElement.style.maxWidth = '100%';
        imageElement.style.borderRadius = '8px';
        imageElement.style.cursor = 'pointer';
        imageElement.onclick = () => {
            const link = document.createElement('a');
            link.href = imageElement.src;
            link.download = `design-${Date.now()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            alert('✅ Design saved successfully!');
        };

        // Display the generated design
        statusMessage.textContent = '✅ Generation complete! Click the image to download.';
        resultsContainer.appendChild(imageElement);

    } catch (error) {
        statusMessage.textContent = `❌ Generation failed: ${error.message}`;
        statusMessage.className = 'status-message error';
        console.error('Generation failed:', error);
    }
}
