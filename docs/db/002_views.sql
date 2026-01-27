CREATE OR REPLACE VIEW v_booking_details AS
SELECT
    b.id AS booking_id,
    b.created_at,
    b.final_price,
    b.status AS booking_status,
    b.client_comment,
    b.manager_comment,
    u.id AS user_id,
    u.email,
    u.full_name,
    u.phone,
    t.id AS tour_id,
    t.name AS tour_name,
    t.country,
    t.city,
    t.start_date,
    t.end_date,
    t.base_price,
    t.currency
FROM bookings b
JOIN users u ON u.id = b.user_id
JOIN tours t ON t.id = b.tour_id;
