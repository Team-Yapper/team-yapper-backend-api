function ErrorPage() {
    return (
    <div className="flex justify-center items-center min-h-[50vh]">
      <p className="text-red-600 bg-red-100 text-lg font-semibold p-2 border border-red-300 rounded">There was an error fetching posts.</p>
    </div>
  );
}

export default ErrorPage;

