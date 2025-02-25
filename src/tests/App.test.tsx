import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../components/App';

describe("App components tests", () => {
    it("First opening", () => {
        render(<App />);
        expect(screen.getByText("Hello")).toBeInTheDocument();
    });
});
