import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import UpdatePostModal from "./UpdatePostModal";

describe("UpdatePostModal", () => {
  const backend = "http://localhost:8000";
  let onClose, onPostUpdated, onPostDeleted;

  beforeEach(() => {
    onClose = vi.fn();
    onPostUpdated = vi.fn();
    onPostDeleted = vi.fn();
    global.fetch = vi.fn();
  });

  const samplePost = {
    id: 42,
    content: "original",
    user_email: "a@b",
    created_at: "now",
  };

  it("renders nothing when closed or no post", () => {
    const { container, rerender } = render(
      <UpdatePostModal
        isOpen={false}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );
    expect(container.firstChild).toBeNull();

    rerender(
      <UpdatePostModal
        isOpen={true}
        post={null}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it("preloads textarea when opened", () => {
    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    const textarea = screen.getByRole("textbox");
    expect(textarea).toHaveValue("original");
  });

  it("calls onClose when esc key is pressed or background clicked", async () => {
    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    // escape
    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);

    // find the outer div by data-testid
    const backdrop = screen.getByTestId("backdrop");
    await userEvent.click(backdrop);
    expect(onClose).toHaveBeenCalledTimes(2);
  });

  it("sends PATCH request and invokes onPostUpdated/onClose when Save is clicked", async () => {
    const updated = { ...samplePost, content: "edited" };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => updated,
    });

    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    const textarea = screen.getByRole("textbox");
    await userEvent.clear(textarea);
    await userEvent.type(textarea, "edited");

    userEvent.click(screen.getByText("Save"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        `${backend}/posts/42`,
        expect.objectContaining({
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ content: "edited" }),
        })
      );
    });

    expect(onPostUpdated).toHaveBeenCalledWith(updated);
    expect(onClose).toHaveBeenCalled();
  });

  it("logs error and does not call callbacks when PATCH fails", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false });
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    const textarea = screen.getByRole("textbox");
    await userEvent.clear(textarea);
    await userEvent.type(textarea, "edited");

    await userEvent.click(screen.getByText("Save"));

    await waitFor(() =>
      expect(consoleSpy).toHaveBeenCalledWith("Update error:", expect.any(Error))
    );

    expect(onPostUpdated).not.toHaveBeenCalled();
    expect(onClose).not.toHaveBeenCalled();

    consoleSpy.mockRestore();
  });

  it("logs error and does not call callbacks when DELETE fails", async () => {
    global.fetch.mockResolvedValueOnce({ ok: false });
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    await userEvent.click(screen.getByText("Delete"));

    await waitFor(() =>
      expect(consoleSpy).toHaveBeenCalledWith("Delete error:", expect.any(Error))
    );

    expect(onPostDeleted).not.toHaveBeenCalled();
    expect(onClose).not.toHaveBeenCalled();

    consoleSpy.mockRestore();
  });

  it("sends DELETE request and invokes onPostDeleted/onClose when Delete is clicked", async () => {
    global.fetch.mockResolvedValueOnce({ ok: true });

    render(
      <UpdatePostModal
        isOpen={true}
        post={samplePost}
        backendUrl={backend}
        onClose={onClose}
        onPostUpdated={onPostUpdated}
        onPostDeleted={onPostDeleted}
      />
    );

    userEvent.click(screen.getByText("Delete"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        `${backend}/posts/42`,
        expect.objectContaining({ method: "DELETE", credentials: "include" })
      );
    });

    expect(onPostDeleted).toHaveBeenCalledWith(42);
    expect(onClose).toHaveBeenCalled();
  });
});