export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to TA AI
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Your AI-powered teaching assistant for university courses
          </p>
          <div className="card max-w-md mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Getting Started</h2>
            <p className="text-gray-600 mb-6">
              Sign in with your university account to access course materials and ask questions.
            </p>
            <button className="btn-primary w-full">
              Sign In with Microsoft
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}