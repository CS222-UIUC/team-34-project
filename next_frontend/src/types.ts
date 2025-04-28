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
  vote_count?: number;
  user_vote?: number;  // 1 for upvote, -1 for downvote, 0 or undefined if no vote
}

export interface Reply {
  id: number;
  content: string;
  timestamp: string;
  author: {
    username: string;
  };
  vote_count?: number;
  user_vote?: number;  // 1 for upvote, -1 for downvote, 0 or undefined if no vote
}

export interface CreatePostData {
  title: string;
  content: string;
  category_id: number;
}

export interface VoteData {
  value: number;  // 1 for upvote, -1 for downvote, 0 to remove vote
} 