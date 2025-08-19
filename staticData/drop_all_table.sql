DO $$ 
DECLARE 
    r RECORD;
BEGIN
    -- Loop through all tables in the public schema
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') 
    LOOP
        -- Drop each table with CASCADE to handle dependencies
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE;';
    END LOOP;
END $$;
-- Script to automatically drop all tables in the public schema of a PostgreSQL database