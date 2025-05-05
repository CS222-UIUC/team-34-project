'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/services/api';
import { Post, Category, Reply } from '@/types';
import UsernameLink from '@/components/UsernameLink';
import VoteButtons from '@/components/VoteButtons';

export default function PostPage({ params }: { params: { postId: string } }) {
  const [post, setPost] = useState<Post | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isClient, setIsClient] = useState(false);
  const router = useRouter();
  const { user, logout } = useAuth();

  // Set isClient state on component mount
  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    // Only run this effect on the client side
    if (!isClient) return;
    
    // Check for user authentication
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
  }, [params.postId, user, router, isClient]);

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

  // Don't render anything during SSR or while checking auth
  if (!isClient || (!user && isClient)) {
    return (
      <div className="min-h-screen flex items-center justify-center text-lg text-gray-700">
        Loading...
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-lg text-gray-700">
        Loading...
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-600 text-lg">
        {error || 'Post not found'}
      </div>
    );
  }

  const category = categories.find((c) => c.id === post.category_id)?.name || 'General';

  return (
    <main className="min-h-screen p-4 bg-gradient-to-br from-white to-blue-50">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={() => router.push('/')}
            className="flex items-center gap-1 text-blue-600 hover:text-blue-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Forum
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

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-start gap-4">
            <div className="flex-grow">
              <div className="flex items-start justify-between mb-4">
                <h1 className="text-3xl font-bold text-gray-900 pr-3">{post.title}</h1>
                <div className="flex-shrink-0">
                  <span className="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm font-medium">
                    {category}
                  </span>
                </div>
              </div>
              
              <div className="flex mt-3">
                <div className="mr-4">
                  <VoteButtons 
                    voteCount={post.vote_count || 0} 
                    userVote={post.user_vote || 0} 
                    onVote={async (value) => {
                      try {
                        const updatedPost = await api.votePost(post.id, { value });
                        setPost({
                          ...post,
                          vote_count: updatedPost.vote_count,
                          user_vote: updatedPost.user_vote
                        });
                      } catch (error) {
                        console.error('Failed to vote on post:', error);
                      }
                    }}
                    vertical={true}
                  />
                </div>
                <div className="flex-1">
                  <p className="text-gray-700 whitespace-pre-line">{post.content}</p>
                  <div className="mt-6 flex justify-between text-sm text-gray-500 border-t pt-4">
                    <span>By <UsernameLink username={post.username} /></span>
                    <span>{new Date(post.created_at).toLocaleString()}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            {post.replies?.length ? `Comments (${post.replies.length})` : 'No comments yet'}
          </h2>
          
          <form
            onSubmit={handleSubmitComment}
            className="mb-8 border-b pb-8"
          >
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Write a comment..."
              className="w-full border border-gray-300 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-400 mb-3"
              rows={4}
            />
            <div className="flex justify-end">
              <button 
                type="submit" 
                className="btn-primary"
                disabled={!newComment.trim()}
              >
                Post Comment
              </button>
            </div>
          </form>

          <div className="space-y-6">
            {!post.replies?.length && (
              <p className="text-center text-gray-500 py-4">
                Be the first to comment on this post!
              </p>
            )}
            
            {post.replies?.map((reply: Reply) => (
              <div
                key={reply.id}
                className="bg-gray-50 p-4 rounded-lg"
              >
                <div className="flex">
                  <div className="mr-3">
                    <VoteButtons 
                      voteCount={reply.vote_count || 0} 
                      userVote={reply.user_vote || 0} 
                      onVote={async (value) => {
                        try {
                          const updatedReply = await api.voteReply(reply.id, { value });
                          setPost({
                            ...post,
                            replies: post.replies.map(r => 
                              r.id === reply.id 
                                ? { ...r, vote_count: updatedReply.vote_count, user_vote: updatedReply.user_vote }
                                : r
                            )
                          });
                        } catch (error) {
                          console.error('Failed to vote on reply:', error);
                        }
                      }}
                    />
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-700">{reply.content}</p>
                    <div className="mt-3 flex justify-between text-sm text-gray-500 border-t border-gray-100 pt-2">
                      <span>By <UsernameLink username={reply.author.username} /></span>
                      <span>{new Date(reply.timestamp).toLocaleString()}</span>
                    </div>
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
