
# RapidReconciler Password Policy

---

## Password Requirements

When the complex password policy is enabled, all user passwords must meet the following criteria:

| Requirement | Detail |
|---|---|
| Minimum length | 8 characters |
| Name restriction | Cannot contain the user's account name or parts of their full name exceeding two consecutive characters |
| Password history | Cannot match any of the last 10 passwords |
| Expiry | Must be changed every 90 days |
| Storage & transmission | Must not be displayed, stored, or transmitted in clear text |

### Character Complexity

Passwords must contain characters from at least **three of the following four** categories:

- English uppercase characters (A through Z)
- English lowercase characters (a through z)
- Base 10 digits (0 through 9)
- Non-alphabetic characters (e.g. `!`, `$`, `#`, `%`)

---

## Logging In

When a user attempts to log in, they will be directed to the **Password Reset** screen if either of the following conditions is met:

1. 90 days have elapsed since their last password change.
2. They click the **"Forgot your password?"** link and then follow the reset link sent to their email.

---

## Resetting the Password

On the Password Reset screen, the new password must conform to the policy outlined above. The **Confirm** button remains disabled until the password meets the 8-character minimum length requirement.

---

## Administration

The RapidReconciler administrator has the ability to assign a temporary password to a new user. Upon first login, the user will be required to reset the temporary password before gaining access to the application.