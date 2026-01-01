import { jwtDecode } from 'jwt-decode';

export interface DecodedToken {
  user_id: string;
  exp: number;
  iat: number;
  [key: string]: any;
}

/**
 * Get the current user ID from the JWT token
 * Using Better Auth session instead of local storage
 */
export const getCurrentUserId = (accessToken?: string): string | null => {
  try {
    // Use the access token from Better Auth session
    if (!accessToken) {
      return null;
    }

    const decoded: DecodedToken = jwtDecode(accessToken);

    // Check if token is expired
    const currentTime = Date.now() / 1000;
    if (decoded.exp < currentTime) {
      return null;
    }

    // Return the user ID from the token
    return decoded.sub || decoded.user_id || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

/**
 * Verify if the current user can access a specific resource
 */
export const verifyUserAccess = (resourceUserId: string, currentUserId: string): boolean => {
  return currentUserId === resourceUserId;
};

/**
 * Check if the auth token exists and is valid
 */
export const isAuthenticated = (accessToken?: string): boolean => {
  return getCurrentUserId(accessToken) !== null;
};