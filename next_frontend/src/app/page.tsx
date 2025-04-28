'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/services/api';
import { Post, Category } from '@/types';
import UsernameLink from '@/components/UsernameLink';
import VoteButtons from '@/components/VoteButtons';

export default function Forum() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();
  const { user, logout } = useAuth();

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchData = async () => {
      try {
        const [postsData, categoriesData] = await Promise.all([
          api.getPosts(),
          api.getCategories()
        ]);
        setPosts(postsData);
        setCategories(categoriesData);
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, router]);

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-lg text-gray-700">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-600 text-lg">
        {error}
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-white to-blue-50 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-10">
          <div className="text-center sm:text-left">
            <h1 className="text-4xl font-bold text-gray-900">Community Forum</h1>
            <p className="text-gray-500 mt-1">Explore and join discussions</p>
          </div>
          <div className="mt-4 sm:mt-0 flex gap-3">
            <button
              onClick={() => router.push(`/user/${user?.username}`)}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg border transition"
            >
              My Account
            </button>
            <button
              onClick={() => router.push('/forum/new')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow transition"
            >
              + New Post
            </button>
            <button
              onClick={handleLogout}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg border transition"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Posts */}
        <div className="grid gap-6">
          {posts.map((post) => {
            const category = categories.find(c => c.id === post.category_id)?.name || 'General';

            return (
              <div
                key={post.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
              >
                <div className="flex">
                  <div className="mr-4">
                    <VoteButtons 
                      voteCount={post.vote_count || 0} 
                      userVote={post.user_vote || 0} 
                      onVote={async (value) => {
                        try {
                          const updatedPost = await api.votePost(post.id, { value });
                          setPosts(
                            posts.map(p => 
                              p.id === post.id 
                                ? { ...p, vote_count: updatedPost.vote_count, user_vote: updatedPost.user_vote }
                                : p
                            )
                          );
                        } catch (error) {
                          console.error('Failed to vote on post:', error);
                        }
                      }}
                      vertical={true}
                    />
                  </div>
                  <div className="flex-1">
                    <div
                      onClick={() => router.push(`/forum/${post.id}`)}
                      className="cursor-pointer"
                    >
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">{post.title}</h3>
                      <p className="text-gray-600 mb-4">{post.content}</p>
                      <div className="flex justify-between text-sm text-gray-400">
                        <span>By <UsernameLink username={post.username} /></span>
                        <span>{new Date(post.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}
