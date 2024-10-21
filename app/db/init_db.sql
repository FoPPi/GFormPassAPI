-- Drop existing objects to ensure clean initialization
DROP FUNCTION IF EXISTS update_delete_date CASCADE;
DROP FUNCTION IF EXISTS select_and_update_question CASCADE;
DROP PROCEDURE IF EXISTS delete_expired_questions CASCADE;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    pub_id TEXT NOT NULL UNIQUE,
    subscription_key TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    active BOOLEAN DEFAULT FALSE NOT NULL,
    day_limit INTEGER DEFAULT 200 NOT NULL,
    end_date DATE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
-- end_date DATE DEFAULT (CURRENT_DATE + INTERVAL '30 days') NOT NULL

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    test_url TEXT NOT NULL,
    question TEXT NOT NULL,
    type TEXT NOT NULL,
    answers TEXT[] NOT NULL,
    delete_date DATE DEFAULT (CURRENT_DATE + INTERVAL '10 days') NOT NULL
);

-- Function to get answer and update their date
CREATE OR REPLACE FUNCTION update_delete_date(question_id INT) RETURNS VOID
    LANGUAGE plpgsql AS $$
BEGIN
    UPDATE questions
    SET delete_date = (CURRENT_DATE + INTERVAL '10 days')
    WHERE id = question_id;
END;
$$;

CREATE OR REPLACE FUNCTION select_and_update_question(in_test_url TEXT , in_question TEXT)
    RETURNS TABLE (type_text TEXT, answers_text TEXT[])
    LANGUAGE plpgsql AS $$
DECLARE
    question_id INT;
BEGIN
    -- Select the answer (this is the action simulating the selection)
    SELECT id, type, answers INTO question_id, type_text, answers_text
    FROM questions
    WHERE question = in_question and test_url = in_test_url
    LIMIT 1;

    -- If something was selected, update delete_date
    IF FOUND THEN
        PERFORM update_delete_date(question_id);
        RETURN NEXT;
    ELSE
        -- If nothing was selected, return 'No matching question found'
        type_text := 'No matching question found';
        answers_text := '{}';
        RETURN NEXT;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_expired_questions()
    LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM questions
    WHERE delete_date < CURRENT_DATE;
END;
$$;

