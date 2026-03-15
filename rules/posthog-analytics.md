# PostHog Analytics Rule

## MANDATORY: Every User-Facing Action MUST Emit a PostHog Event

When creating or modifying any component/screen that involves an **authenticated user action**, you MUST include a PostHog analytics event. This is not optional — it is a project requirement for consistent analytics coverage.

## When to Add Events

Add a `posthog.capture()` call when ANY of these occur:

| Trigger | Example Event Name |
|---------|-------------------|
| User creates something | `habit_created`, `peer_habit_created`, `group_habit_created` |
| User completes/toggles something | `habit_toggled`, `habit_value_updated` |
| User deletes something | `habit_deleted`, `entry_deleted` |
| User signs in/out | `user_signed_in`, `sign_out` |
| User views a conversion screen | `paywall_viewed`, `onboarding_step_viewed` |
| User completes a flow | `onboarding_completed`, `premium_purchased` |
| User joins/leaves something | `group_habit_joined`, `peer_habit_accepted` |
| User shares/invites | `invite_sent`, `share_link_created` |
| User interacts with a social feature | `nudge_sent`, `peer_habit_nudge_sent` |

## How to Implement

### Import Pattern

```typescript
import { posthog } from '@/services/posthog';
```

Do NOT use `usePostHog()` hook unless you specifically need the React context instance (e.g., for `posthog.identify` or `posthog.reset` in layout-level components). For event capture, use the singleton import.

### Event Naming Convention

- **snake_case** always: `habit_created`, NOT `habitCreated`
- **verb_past_tense** for actions: `created`, `toggled`, `viewed`, `completed`, `deleted`, `sent`
- **noun_first**: `habit_created`, NOT `created_habit`

### Required Properties

Every event MUST include properties that provide context:

```typescript
// GOOD — actionable properties
posthog.capture('habit_created', {
  habit_type: type,        // 'check' | 'number'
  goal_type: goalType,     // 'at_least' | 'at_most'
  frequency: frequency,    // 'daily' | 'weekly' | 'monthly'
});

// BAD — no properties
posthog.capture('habit_created');
```

### Minimum Property Guidelines

| Event Category | Required Properties |
|---------------|-------------------|
| Creation events | `*_type`, relevant config fields |
| Toggle/update events | `habit_id`, `date`, `value` (if numeric) |
| Auth events | `method: 'google' \| 'apple' \| 'email' \| 'anonymous'` |
| Premium events | `plan`, `placement`, `platform` |
| Social events | `group_id` or `peer_group_id` |
| Navigation/view events | `screen_name`, `source` (where they came from) |

### Placement in Code

Capture events **after successful completion**, not before:

```typescript
// GOOD — capture after success
const result = await createHabit(habitData);
if (result) {
  posthog.capture('habit_created', { habit_type: type });
}

// BAD — capture before knowing if it succeeded
posthog.capture('habit_created', { habit_type: type });
await createHabit(habitData); // might fail
```

### No PII Rule

NEVER send personally identifiable information in events:

```typescript
// FORBIDDEN — PII in events
posthog.capture('user_signed_in', { email: user.email, name: user.displayName });

// ALLOWED — non-PII only
posthog.capture('user_signed_in', { method: 'google' });
```

User identification is handled ONLY in `app/_layout.tsx` via `posthog.identify(user.uid)`.

## Registered Events Reference

These events are currently tracked. When adding new features, follow this pattern:

| Event | File | Properties |
|-------|------|-----------|
| `user_signed_in` | `app/auth.tsx` | `method` |
| `habit_created` | `app/create-habit.tsx` | `habit_type`, `goal_type` |
| `habit_edited` | `app/create-habit.tsx` | `habit_id`, `habit_type` |
| `habit_toggled` | `contexts/habits/EntryContext.tsx` | `habit_id`, `date` |
| `habit_value_updated` | `contexts/habits/EntryContext.tsx` | `habit_id`, `date`, `value` |
| `paywall_viewed` | `components/premium/LiquidGlassPaywall.tsx` | `placement` |
| `premium_purchased` | `components/premium/LiquidGlassPaywall.tsx` | `plan`, `placement`, `platform` |
| `peer_habit_created` | `app/create-peer-habit.tsx` | `relationship_type`, `habit_type` |
| `group_habit_joined` | `app/join-group-habit/[code].tsx` | `group_id` |
| `sign_out` | `app/settings.tsx` | — |
| `onboarding_completed` | `screens/OnboardingScreen.tsx` | `skipped` |

## Self-Check

When reviewing code or creating a new screen/component, ask:

1. Does this component let the user **do** something? → Add an event
2. Does this component show a **conversion surface** (paywall, signup, upgrade)? → Add a `*_viewed` event
3. Does this component **modify user data**? → Add a `*_created`/`*_updated`/`*_deleted` event
4. Is the event captured **after** the action succeeds? → Yes, always
5. Are the properties **non-PII** and **actionable**? → No emails, names, or phone numbers
