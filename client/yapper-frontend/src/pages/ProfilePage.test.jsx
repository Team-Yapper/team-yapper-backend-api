import { render, screen, fireEvent } from "@testing-library/react";
import ProfilePage from "./ProfilePage";

// mock react-router useNavigate so the component can call it without a router
const navigateMock = vi.fn();
vi.mock("react-router-dom", () => ({
  ...vi.importActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

// stub the sub‑components so they don’t pull in extra code
vi.mock("../components/Navbar.jsx", () => ({
  default: () => <div>navbar</div>,
}));
vi.mock("./UpdatePostModal", () => ({
  default: () => null, // we never open the modal in these tests
}));

beforeEach(() => {
  // reset navigate mock and replace global fetch
  navigateMock.mockReset();
  global.fetch = vi.fn();
});

test("shows error message when fetching user fails", async () => {
  // first call for /user fails
  global.fetch.mockResolvedValueOnce({ ok: false });

  render(<ProfilePage />);

  expect(
    await screen.findByText(/failed to load posts\./i)
  ).toBeInTheDocument();
});

test("renders profile info and " +
     "'No posts to display.' when logged in with no posts", async () => {
  const fakeUser = { id: 5, email: "john@example.com", bio: "hello" };

  global.fetch
    .mockResolvedValueOnce({ ok: true, json: async () => fakeUser })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ posts: [] }) });

  render(<ProfilePage />);

  expect(await screen.findByText("john")).toBeInTheDocument();
  expect(screen.getByText("john@example.com")).toBeInTheDocument();
  expect(screen.getByText("hello")).toBeInTheDocument();
  expect(screen.getByText(/no posts to display/i)).toBeInTheDocument();
});

test("displays user posts when available and allows update button", async () => {
  const fakeUser = { id: 9, email: "alice@example.com" };
  const fakePosts = [{ id: 42, content: "my post" }];

  global.fetch
    .mockResolvedValueOnce({ ok: true, json: async () => fakeUser })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ posts: fakePosts }) });

  render(<ProfilePage />);

  expect(await screen.findByText(/your posts/i)).toBeInTheDocument();
  expect(screen.getByText("my post")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /update/i })).toBeInTheDocument();
});

// optionally assert navigation when home button clicked
// note: navigateMock is returned from useNavigate

it("navigates home when back button is clicked", async () => {
  global.fetch.mockResolvedValueOnce({ ok: false }); // cause early error

  render(<ProfilePage />);

  const homeBtn = await screen.findByText(/home/i);
  fireEvent.click(homeBtn);
  expect(navigateMock).toHaveBeenCalledWith("/");
});
