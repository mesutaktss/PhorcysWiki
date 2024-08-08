from flask import Flask, render_template, request, jsonify
from phorcys import ProcessText
from phorcys import TextGenerator
from phorcys import ProcessWithAI
import ollama

app = Flask(__name__)

MODELNAME = "brooqs/mistral-turkish-v2"

FUNCTIONS = {
    'upperText': ProcessText.upperText,
    'lowerText': ProcessText.lowerText,
    'removePunc': ProcessText.removePunc,
    'accentMarkRemove': ProcessText.accentMarkRemove,
    'numToTRText': ProcessText.numToTRText,     
    'removeNumber': ProcessText.removeNumber,
    'normalizeChars': ProcessText.normalizeChars,
    'wordCounter': ProcessText.wordCounter,
    'wordExtractor': ProcessText.wordExtractor, 
    'sentenceCounter': ProcessText.sentenceCounter,
    'avarageWordCountPerSentence': ProcessText.avarageWordCountPerSentence,
    'syllableCounter': ProcessText.syllableCounter,
    'reabilityTime': ProcessText.reabilityTime,
    'readabilityScore': ProcessText.readabilityScore,
    'frequencyCalculator': ProcessText.frequencyCalculator, 
    'phoneticTransform': ProcessText.phoneticTransform,
    'sentenceTokenizer': ProcessText.sentenceTokenizer,
    'findIdioms': ProcessText.findIdioms,
    'deasciify': ProcessText.deasciify,
    'NewsAnalysis': lambda text: ProcessWithAI.NewsAnalysis(text=text),
    'OffensiveLanguageAnalysis': lambda text: ProcessWithAI.OffensiveLanguageAnalysis(text=text),
    'DetailedEmotionAnalysis': lambda text: ProcessWithAI.DetailedEmotionAnalysis(text=text),
    'SimpleEmotionAnalysis': lambda text: ProcessWithAI.SimpleEmotionAnalysis(text=text),     
    'BullyingAnalysis': lambda text: ProcessWithAI.BullyingAnalysis(text=text),
    'TranslateToTurkish': lambda text: ProcessWithAI.TranslateToTurkish(text=text),
    'TranslateToEnglish': lambda text: ProcessWithAI.TranslateToEnglish(text=text),
    'NERAnalysis': lambda text: ProcessWithAI.NERAnalysis(text=text),
    'sentenceCounter': lambda text: ProcessWithAI.sentenceCounter(text=text),
    'avarageWordCountPerSentence': lambda text: ProcessWithAI.avarageWordCountPerSentence(text=text),
    'EntityBasedSentimentAnalysis': lambda text: ProcessWithAI.EntityBasedSentimentAnalysis(text=text)
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Abyss')
def AbyssPage():
    return render_template('Abyss.html')

@app.route('/AIProcessText')
def AIProcessTextPage():
    return render_template('AIProcessText.html')

@app.route('/GenerateText')
def GenerateTextPage():
    return render_template('GenerateText.html')


@app.route('/Model')
def ModelPage():
    return render_template('Model.html')


@app.route('/ProcessMedia')
def ProcessMediaPage():
    return render_template('ProcessMedia.html')


@app.route('/ProcessText')
def ProcessTextPage():
    return render_template('ProcessText.html')
    
@app.route('/App', methods=['GET', 'POST'])
def App():
    result = ''
    if request.method == 'POST':
        user_input = str(request.form['text'])
        function_choice = request.form['function']
        process_by_sentences = 'process_sentences' in request.form

        if process_by_sentences:
            # Cümlelere ayır
            sentences = ProcessText.sentenceTokenizer(user_input)
            # Her cümleye seçilen fonksiyonu uygula
            function = FUNCTIONS.get(function_choice, lambda x: x)
            results = [function(sentence) for sentence in sentences]
            result = '\n'.join(results)
        else:
            # Tek parça metne fonksiyon uygula
            function = FUNCTIONS.get(function_choice, lambda x: x)
            result = function(user_input)

    return render_template('App.html', result=result)

@app.route('/Chat')
def chat():
    return render_template('chat.html')

@app.route('/Chat-api', methods=['POST'])
def chat_api():
    if request.is_json:
        user_message = request.json.get('message')
        bot_response = TextGenerator.generateResponse(model_name=MODELNAME, prompt=user_message)
        return jsonify({'response': bot_response})
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':
    app.run(debug=True)
