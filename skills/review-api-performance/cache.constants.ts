/**
 * Cache TTL Constants
 *
 * Use these constants instead of raw seconds values.
 * Grade determines data freshness priority:
 *   - VERY_HIGH: Data must be near real-time (20 min)
 *   - HIGH: Data can be slightly stale (2 hours)
 *   - MEDIUM: Relaxed freshness (6 hours)
 *   - LOW: Data can be very stale (24 hours)
 *
 * @example
 * ```typescript
 * import { CacheTTL } from 'src/common/constants/cache.constants';
 *
 * @Cache('user_session_{userId}', '', CacheTTL.VERY_HIGH)
 * async getActiveSession(userId: Types.ObjectId) { }
 * ```
 */
export const CacheTTL = {
  /** 🔴 Near real-time data - 20 minutes (1200 seconds) */
  VERY_HIGH: 1200,

  /** 🟡 Eventual consistency - 2 hours (7200 seconds) */
  HIGH: 7200,

  /** 🔵 Relaxed consistency - 6 hours (21600 seconds) */
  MEDIUM: 21600,

  /** 🟢 Lazy consistency - 24 hours (86400 seconds) */
  LOW: 86400,
} as const;

export type CacheTTLValue = (typeof CacheTTL)[keyof typeof CacheTTL];
