import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

interface VoteButtonsProps {
  voteCount: number;
  userVote: number;
  onVote: (value: number) => Promise<void>;
  vertical?: boolean;
}

export default function VoteButtons({ voteCount, userVote, onVote, vertical = false }: VoteButtonsProps) {
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();
  const router = useRouter();

  const handleVote = async (value: number) => {
    if (!user) {
      router.push('/login');
      return;
    }

    if (isLoading) return;

    try {
      setIsLoading(true);
      // If user clicked the same button that's already active, remove the vote
      const newValue = userVote === value ? 0 : value;
      await onVote(newValue);
    } catch (error) {
      console.error('Failed to vote:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const containerClasses = vertical 
    ? 'flex flex-col items-center gap-1' 
    : 'flex items-center gap-2';

  return (
    <div className={containerClasses}>
      <button
        onClick={() => handleVote(1)}
        disabled={isLoading}
        className={`p-1 rounded-full transition-colors ${
          userVote === 1
            ? 'text-blue-600 bg-blue-50'
            : 'text-gray-400 hover:text-blue-500 hover:bg-blue-50'
        }`}
        aria-label="Upvote"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-5 h-5"
        >
          <path d="M12 4l8 8h-6v8h-4v-8H4z" />
        </svg>
      </button>

      <span className={`font-medium ${
        voteCount > 0 
          ? 'text-blue-600' 
          : voteCount < 0 
            ? 'text-red-600' 
            : 'text-gray-500'
      }`}>
        {voteCount}
      </span>

      <button
        onClick={() => handleVote(-1)}
        disabled={isLoading}
        className={`p-1 rounded-full transition-colors ${
          userVote === -1
            ? 'text-red-600 bg-red-50'
            : 'text-gray-400 hover:text-red-500 hover:bg-red-50'
        }`}
        aria-label="Downvote"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-5 h-5"
        >
          <path d="M12 20l-8-8h6V4h4v8h6z" />
        </svg>
      </button>
    </div>
  );
} 