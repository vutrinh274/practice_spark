Given a table `events` with columns `event_id`, `user_id`, `event_type`, and `properties`, where `properties` is a JSON string containing the keys `page`, `duration`, and `referrer`:

Parse the `properties` JSON column and extract each key as a separate column.

Return columns: `event_id`, `user_id`, `event_type`, `page`, `duration` (INT), `referrer`.

Order by `event_id` ascending.
