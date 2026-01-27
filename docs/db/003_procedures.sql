CREATE OR REPLACE FUNCTION auto_cancel_bookings(
    p_hours INTEGER DEFAULT 24
) RETURNS void AS $$
BEGIN
    UPDATE bookings
    SET status = 'Cancelled',
        manager_comment = 'Auto-cancelled due to timeout'
    WHERE status = 'Created'
      AND created_at < (NOW() - (p_hours || ' hours')::interval);
END;
$$ LANGUAGE plpgsql;
