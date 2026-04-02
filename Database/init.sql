DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'transactions') THEN
        RAISE EXCEPTION 'Table transactions does not exist. Run schema.sql first.';
    END IF;
    RAISE NOTICE 'Supabase schema verified successfully.';
END $$;