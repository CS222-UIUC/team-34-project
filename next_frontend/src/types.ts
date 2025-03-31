export interface Category {
  id: number;
  name: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  category_id: number;
  user_id: number;
  username: string;
  replies: Reply[];
}

export interface Reply {
  id: number;
  content: string;
  created_at: string;
  user_id: number;
  username: string;
  post_id: number;
}

export interface CreatePostData {
  title: string;
  content: string;
  category_id: number;
} 