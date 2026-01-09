import { useState } from 'react'

function App() {
  const [prompt, setPrompt] = useState('')

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-2xl p-8">
        <h1 className="text-4xl font-bold text-center mb-2 text-gray-800">
          💨 Fart Generator
        </h1>
        <p className="text-center text-gray-600 mb-8">
          AI-Powered Realistic Fart Sound Generation
        </p>

        <div className="space-y-6">
          <div>
            <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
              Describe your desired fart sound
            </label>
            <textarea
              id="prompt"
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
              placeholder="e.g., a long, rumbling fart..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <button
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors shadow-lg"
            disabled={!prompt.trim()}
          >
            Generate Sound
          </button>

          <div className="text-center text-sm text-gray-500">
            <p>Coming soon: Real-time generation with WebSocket!</p>
            <p className="mt-2">Backend API: <a href="http://localhost:8000/api/docs" target="_blank" className="text-purple-600 hover:underline">http://localhost:8000/api/docs</a></p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
