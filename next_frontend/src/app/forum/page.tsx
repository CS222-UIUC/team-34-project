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
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await api.getCurrentUser();
      } catch (err) {
        console.log(err);
        router.push('/');
      }
    };
    checkAuth();
  }, [router]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [postsData, categoriesData] = await Promise.all([
          api.getPosts(),
          api.getCategories()
        ]);
        setPosts(postsData);
        setCategories(categoriesData);
      } catch (err) {
        console.log(err);
        setError('Failed to load data');
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const newPost = await api.createPost({
        title,
        content,
        category_id: parseInt(categoryId)
      });
      setPosts([newPost, ...posts]);
      setTitle('');
      setContent('');
      setCategoryId('');
    } catch (err) {
      console.log(err);
      setError('Failed to create post');
    }
  };

  const handleLogout = async () => {
    try {
      await api.logout();
      router.push('/');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  const filteredPosts = selectedCategory
    ? posts.filter(post => post.category_id === selectedCategory)
    : posts;

  return (
    <main className="min-h-screen p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Forum</h1>
          <div className="flex gap-3">
            <button
              onClick={() => router.push(`/user/${user?.username}`)}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg border transition"
            >
              My Account
            </button>
            <button
              onClick={handleLogout}
              className="btn-secondary"
            >
              Logout
            </button>
          </div>
        </div>

        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Post</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="input-field"
                required
              />
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select
                id="category"
                value={categoryId}
                onChange={(e) => setCategoryId(e.target.value)}
                className="input-field"
                required
              >
                <option value="">Select a category</option>
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
                Content
              </label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="input-field min-h-[150px]"
                required
              />
            </div>

            {error && (
              <div className="text-red-600 text-sm">{error}</div>
            )}

            <button type="submit" className="btn-primary">
              Create Post
            </button>
          </form>
        </div>

        <div className="flex gap-4 mb-6 overflow-x-auto pb-2">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
              selectedCategory === null
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Posts
          </button>
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                selectedCategory === category.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        <div className="space-y-4">
          {filteredPosts.map((post) => (
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
          ))}
        </div>
      </div>
    </main>
  );
} 