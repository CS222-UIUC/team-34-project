'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/services/api';
import { Post, Category, Reply } from '@/types';
import UsernameLink from '@/components/UsernameLink';

export default function PostPage({ params }: { params: { postId: string } }) {
  const [post, setPost] = useState<Post | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [newComment, setNewComment] = useState('');
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
        const [postData, categoriesData] = await Promise.all([
          api.getPost(params.postId),
          api.getCategories(),
        ]);
        setPost(postData);
        setCategories(categoriesData);
      } catch (err) {
        setError('Failed to load post');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params.postId, user, router]);

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      await api.createReply(params.postId, { content: newComment });
      const updatedPost = await api.getPost(params.postId);
      setPost(updatedPost);
      setNewComment('');
    } catch (err) {
      setError('Failed to submit comment');
      console.error(err);
    }
  };

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
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-600">
        {error || 'Post not found'}
      </div>
    );
  }

  return (
    <main className="min-h-screen p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={() => router.push('/')}
            className="text-blue-600 hover:text-blue-800"
          >
            ← Back to Forum
          </button>
          <div className="flex gap-3">
            <button
              onClick={() => router.push(`/user/${user?.username}`)}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg border transition"
            >
              My Account
            </button>
            <button onClick={handleLogout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>

        <div className="card mb-8">
          <div className="flex justify-between items-start">
            <div className="w-full">
              <h1 className="text-3xl font-bold text-gray-900">{post.title}</h1>
              <p className="text-gray-700 mt-4">{post.content}</p>
              <div className="mt-6 flex justify-between text-sm text-gray-400">
                <span>By <UsernameLink username={post.username} /></span>
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
            </div>
            <span className="ml-4 px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm font-medium whitespace-nowrap">
              {categories.find((c) => c.id === post.category_id)?.name}
            </span>
          </div>
        </div>

        <section>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Comments</h2>
          <div className="space-y-4">
            {post.replies?.map((reply: Reply) => (
              <div
                key={reply.id}
                className="card hover:shadow-md transition-shadow"
              >
                <p className="text-gray-700">{reply.content}</p>
                <div className="mt-2 flex justify-between text-sm text-gray-400">
                  <span>By <UsernameLink username={reply.author.username} /></span>
                  <span>{new Date(reply.timestamp).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>

          <form
            onSubmit={handleSubmitComment}
            className="mt-8 bg-white p-4 rounded-lg shadow-md space-y-4"
          >
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Write a comment..."
              className="w-full border border-gray-300 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
              rows={4}
            />
            <button type="submit" className="btn-primary">
              Submit Comment
            </button>
          </form>
        </section>
      </div>
    </main>
  );
}
