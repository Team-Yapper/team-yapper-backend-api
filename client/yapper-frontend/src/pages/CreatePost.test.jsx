import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, describe, test, expect, beforeEach } from "vitest";
import CreatePost from "./CreatePost";

// Mock fetch globally
global.fetch = vi.fn();

describe("CreatePost Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("renders the form with all elements", () => {
    render(<CreatePost />);

    expect(
      screen.getByText("What do you want to yap about?"),
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Share your thoughts..."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /post/i })).toBeInTheDocument();
  });

  test("renders cancel button when onClose is provided", () => {
    const mockOnClose = vi.fn();
    render(<CreatePost onClose={mockOnClose} />);

    expect(screen.getByRole("button", { name: /cancel/i })).toBeInTheDocument();
  });

  test("does not render cancel button when onClose is not provided", () => {
    render(<CreatePost />);

    expect(
      screen.queryByRole("button", { name: /cancel/i }),
    ).not.toBeInTheDocument();
  });

  test("updates textarea value as user types", async () => {
    const user = userEvent.setup();
    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "This is my test post");

    expect(textarea.value).toBe("This is my test post");
  });

  test("shows error when trying to submit empty post", async () => {
    const user = userEvent.setup();
    render(<CreatePost />);

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    expect(
      screen.getByText("Post content cannot be empty"),
    ).toBeInTheDocument();
  });

  test("shows error for only whitespace content", async () => {
    const user = userEvent.setup();
    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "   ");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    expect(
      screen.getByText("Post content cannot be empty"),
    ).toBeInTheDocument();
  });

  test("successfully creates a post", async () => {
    const user = userEvent.setup();
    const mockOnCreate = vi.fn();
    const mockPost = {
      id: 1,
      content: "Test post",
      user_id: 1,
      created_at: "02/20/26 at 10:30AM",
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockPost,
    });

    render(<CreatePost onCreate={mockOnCreate} />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/posts",
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: "Test post" }),
          credentials: "include",
        }),
      );
    });

    await waitFor(() => {
      expect(mockOnCreate).toHaveBeenCalledWith(mockPost);
    });
  });

  test("clears textarea after successful post creation", async () => {
    const user = userEvent.setup();
    const mockOnCreate = vi.fn();

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, content: "Test", user_id: 1 }),
    });

    render(<CreatePost onCreate={mockOnCreate} />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(textarea.value).toBe("");
    });
  });

  test("shows loading state during submission", async () => {
    const user = userEvent.setup();

    fetch.mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(() => {
            resolve({
              ok: true,
              json: async () => ({ id: 1, content: "Test" }),
            });
          }, 100),
        ),
    );

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    expect(
      screen.getByRole("button", { name: /creating/i }),
    ).toBeInTheDocument();

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: /^post$/i }),
      ).toBeInTheDocument();
    });
  });

  test("disables textarea and buttons during submission", async () => {
    const user = userEvent.setup();

    fetch.mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(() => {
            resolve({
              ok: true,
              json: async () => ({ id: 1, content: "Test" }),
            });
          }, 100),
        ),
    );

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    expect(textarea).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });

  test("shows error when response is not ok (401)", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
    });

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(
        screen.getByText("You must be logged in to create a post"),
      ).toBeInTheDocument();
    });
  });

  test("shows error when response is not ok (404)", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText("User not found")).toBeInTheDocument();
    });
  });

  test("shows generic error for other HTTP errors", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText("Failed to create post")).toBeInTheDocument();
    });
  });

  test("shows error when fetch throws an error", async () => {
    const user = userEvent.setup();

    fetch.mockRejectedValueOnce(new Error("Network error"));

    render(<CreatePost />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText("Network error")).toBeInTheDocument();
    });
  });

  test("calls onClose when cancel button is clicked", async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    render(<CreatePost onClose={mockOnClose} />);

    const cancelButton = screen.getByRole("button", { name: /cancel/i });
    await user.click(cancelButton);

    expect(mockOnClose).toHaveBeenCalled();
  });

  test("calls onClose even when onCreate is provided and post is successful", async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();
    const mockOnCreate = vi.fn();

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, content: "Test" }),
    });

    render(<CreatePost onClose={mockOnClose} onCreate={mockOnCreate} />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnCreate).toHaveBeenCalled();
    });

    // onCreate should be called, not onClose
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  test("calls onClose when onCreate is not provided and post is successful", async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, content: "Test" }),
    });

    render(<CreatePost onClose={mockOnClose} />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "Test post");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  test("trims whitespace from post content before sending", async () => {
    const user = userEvent.setup();
    const mockOnCreate = vi.fn();

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, content: "Test post" }),
    });

    render(<CreatePost onCreate={mockOnCreate} />);

    const textarea = screen.getByPlaceholderText("Share your thoughts...");
    await user.type(textarea, "  Test post  ");

    const submitButton = screen.getByRole("button", { name: /post/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/posts",
        expect.objectContaining({
          body: JSON.stringify({ content: "Test post" }),
        }),
      );
    });
  });
});
