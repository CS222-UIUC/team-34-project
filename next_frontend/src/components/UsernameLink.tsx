import Link from 'next/link';

interface UsernameLinkProps {
  username: string;
  className?: string;
}

export default function UsernameLink({ username, className = '' }: UsernameLinkProps) {
  return (
    <Link 
      href={`/user/${username}`}
      className={`text-blue-600 hover:text-blue-800 hover:underline ${className}`}
    >
      {username}
    </Link>
  );
} 