import { Post, Category, CreatePostData } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

export interface User {
  id: number;
  username: string;
}

export interface Reply {
  id: number;
  content: string;
  timestamp: string;
  author: User;
}

export const api = {
  async register(username: string, password: string) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Registration failed');
    }

    return response.json();
  },

  async login(username: string, password: string) {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Login failed');
    }

    return response.json();
  },

  async logout() {
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Logout failed');
    }

    return response.json();
  },

  async getCurrentUser() {
    const response = await fetch(`${API_URL}/auth/user`, {
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Not authenticated');
    }

    return response.json();
  },

  async getPosts(): Promise<Post[]> {
    const response = await fetch(`${API_URL}/posts`, {
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch posts');
    }

    const data = await response.json();
    return data.map((post: any) => ({
      id: post.id,
      title: post.title,
      content: post.content,
      created_at: post.created_at || post.timestamp,
      category_id: post.category_id || post.category?.id,
      user_id: post.user_id || post.author?.id,
      username: post.username || post.author?.username,
      replies: post.replies || []
    }));
  },

  async createPost(data: CreatePostData): Promise<Post> {
    const response = await fetch(`${API_URL}/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to create post');
    }

    const post = await response.json();
    return {
      id: post.id,
      title: post.title,
      content: post.content,
      created_at: post.created_at || post.timestamp,
      category_id: post.category_id || post.category?.id,
      user_id: post.user_id || post.author?.id,
      username: post.username || post.author?.username,
      replies: post.replies || []
    };
  },

  async getCategories(): Promise<Category[]> {
    const response = await fetch(`${API_URL}/categories`, {
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }

    return response.json();
  }
};