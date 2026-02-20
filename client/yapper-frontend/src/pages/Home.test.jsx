import { render, screen } from "@testing-library/react";
import Home from "./Home";

// stub the sub‑components so they don’t pull in extra code
vi.mock("../components/Navbar.jsx", () => ({
  default: () => <div>navbar</div>,
}));
vi.mock("./CreatePost", () => ({
  default: () => null,          // we never open the modal in these tests
}));
vi.mock("./ErrorPage", () => ({
  default: () => <div>error</div>,
}));

beforeEach(() => {
  // replace the global fetch with a fresh mock each time
  global.fetch = vi.fn();
});

test("renders ErrorPage when the posts request fails", async () => {
  // first call is /user, second call is /posts
  global.fetch
    .mockResolvedValueOnce({ ok: true })    // user endpoint
    .mockResolvedValueOnce({ ok: false }); // posts endpoint

  render(<Home />);

  expect(await screen.findByText("error")).toBeInTheDocument();
});

test('shows "No posts available." and no + button when nobody is logged in', async () => {
  global.fetch
    .mockResolvedValueOnce({ ok: false })                    // not logged in
    .mockResolvedValueOnce({ ok: true, json: async () => [] }); // empty post list

  render(<Home />);

  expect(await screen.findByText(/no posts available/i)).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "+" })).toBeNull();
});

test("displays the post content and the + button when logged in", async () => {
  const fake = [
    { id: 1, content: "hello", user_email: "x@x", created_at: "now" },
  ];

  global.fetch
    .mockResolvedValueOnce({ ok: true })                     // logged in
    .mockResolvedValueOnce({ ok: true, json: async () => fake }); // posts

  render(<Home />);

  expect(await screen.findByText("hello")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "+" })).toBeInTheDocument();
});