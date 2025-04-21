'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

// Mock data for the user profile
const mockUserProfile = {
  username: 'johndoe',
  fullName: 'John Doe',
  joinedDate: '2023-01-15',
  bio: 'Software developer and tech enthusiast. Love to share knowledge and learn from others.',
  stats: {
    posts: 42,
    comments: 156,
    likes: 289,
    followers: 123,
    following: 45
  },
  recentPosts: [
    {
      id: 1,
      title: 'Understanding React Hooks',
      content: 'A deep dive into React Hooks and their usage patterns...',
      category: 'Programming',
      date: '2023-12-15',
      likes: 24,
      comments: 8
    },
    {
      id: 2,
      title: 'Best Practices for API Design',
      content: 'Some tips and tricks for designing robust APIs...',
      category: 'Backend',
      date: '2023-12-10',
      likes: 18,
      comments: 5
    },
    {
      id: 3,
      title: 'CSS Grid vs Flexbox',
      content: 'When to use Grid and when to use Flexbox...',
      category: 'Frontend',
      date: '2023-12-05',
      likes: 32,
      comments: 12
    }
  ],
  badges: [
    { name: 'Early Adopter', icon: '🚀' },
    { name: 'Top Contributor', icon: '🏆' },
    { name: 'Helpful User', icon: '🤝' }
  ]
};

export default function UserProfile({ params }: { params: { username: string } }) {
  const router = useRouter();
  const { user } = useAuth();

  if (!user) {
    router.push('/login');
    return null;
  }

  return (
    <main className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Back button */}
        <button
          onClick={() => router.back()}
          className="mb-6 text-blue-600 hover:text-blue-800 flex items-center"
        >
          <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back
        </button>

        {/* Profile Header */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-start justify-between">
            <div className="flex items-center">
              <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center text-4xl font-bold text-blue-600">
                {mockUserProfile.username.charAt(0).toUpperCase()}
              </div>
              <div className="ml-6">
                <h1 className="text-2xl font-bold text-gray-900">{mockUserProfile.fullName}</h1>
                <p className="text-gray-600">@{mockUserProfile.username}</p>
                <p className="text-gray-500 text-sm mt-2">
                  Joined {new Date(mockUserProfile.joinedDate).toLocaleDateString()}
                </p>
              </div>
            </div>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Follow
            </button>
          </div>
          <p className="mt-4 text-gray-700">{mockUserProfile.bio}</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-5 gap-4 mb-6">
          {Object.entries(mockUserProfile.stats).map(([key, value]) => (
            <div key={key} className="bg-white rounded-lg p-4 text-center shadow-sm">
              <div className="text-2xl font-bold text-gray-900">{value}</div>
              <div className="text-sm text-gray-500 capitalize">{key}</div>
            </div>
          ))}
        </div>

        {/* Badges */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Badges</h2>
          <div className="flex gap-4">
            {mockUserProfile.badges.map((badge, index) => (
              <div key={index} className="flex items-center bg-gray-50 rounded-lg px-4 py-2">
                <span className="text-2xl mr-2">{badge.icon}</span>
                <span className="text-gray-700">{badge.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Posts */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Posts</h2>
          <div className="space-y-4">
            {mockUserProfile.recentPosts.map((post) => (
              <div
                key={post.id}
                className="border border-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => router.push(`/forum/${post.id}`)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">{post.title}</h3>
                    <p className="text-gray-600 mt-1 line-clamp-2">{post.content}</p>
                  </div>
                  <span className="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm">
                    {post.category}
                  </span>
                </div>
                <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-4">
                    <span>{new Date(post.date).toLocaleDateString()}</span>
                    <span className="flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                      </svg>
                      {post.likes}
                    </span>
                    <span className="flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                      {post.comments}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
} 