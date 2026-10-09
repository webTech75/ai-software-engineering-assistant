import { useEffect, useState } from "react";
import {
  createProjectRequest,
  getProjectsRequest,
} from "@/api/requests";
import { useNavigate } from "react-router-dom";

interface Project {
  id: number;
  name: string;
  description?: string | null;
}

export function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  async function loadProjects() {
    try {
      setError("");
      const data = await getProjectsRequest();
      setProjects(data);
    } catch {
      setError("Unable to load projects. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }

    try {
      setCreating(true);
      setError("");
      setSuccess("");

      const project = await createProjectRequest({
        name: name.trim(),
        description: description.trim() || undefined,
      });

      setProjects((current) => [...current, project]);
      setName("");
      setDescription("");
      setSuccess("Project created successfully.");
    } catch {
      setError("Unable to create project. Please try again.");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <section>
        <h1 className="text-3xl font-bold">
          AI Software Engineering Assistant
        </h1>
        <p className="mt-2 text-muted-foreground">
          Create a project to organize your engineering tasks.
        </p>
      </section>

      <section className="rounded-xl border p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">
          Create a project
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="project-name" className="block text-sm font-medium">
              Project name
            </label>
            <input
              id="project-name"
              type="text"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="My software project"
              required
              className="w-full rounded-lg border p-3"
            />
          </div>

          <div className="space-y-2">
            <label
              htmlFor="project-description"
              className="block text-sm font-medium"
            >
              Description (optional)
            </label>
            <textarea
              id="project-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Describe what you want to build..."
              rows={4}
              className="w-full rounded-lg border p-3"
            />
          </div>

          <button
            type="submit"
            disabled={creating || !name.trim()}
            className="rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {creating ? "Creating..." : "Create project"}
          </button>
        </form>

        {error && (
          <p role="alert" className="mt-4 text-sm text-red-600">
            {error}
          </p>
        )}

        {success && (
          <p className="mt-4 text-sm text-green-600">
            {success}
          </p>
        )}
      </section>

      <section className="rounded-xl border p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">Your projects</h2>

        {loading ? (
          <p>Loading projects...</p>
        ) : projects.length === 0 ? (
          <p className="text-muted-foreground">
            You haven't created any projects yet.
          </p>
        ) : (
          <div className="space-y-3">
            {projects.map((project) => (
              <article
                key={project.id}
                role="button"
                tabIndex={0}
                onClick={() => navigate(`/projects/${project.id}`)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    navigate(`/projects/${project.id}`);
                  }
                }}
                className="cursor-pointer rounded-lg border p-4 hover:bg-gray-50"
              >
                <h3 className="font-semibold">{project.name}</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {project.description || "No description provided."}
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Project ID: {project.id}
                </p>
              </article>
            ))}
          </div>
        )}

        <button
          type="button"
          onClick={loadProjects}
          disabled={loading}
          className="mt-4 rounded-lg border px-4 py-2 hover:bg-gray-100 disabled:opacity-50"
        >
          Refresh projects
        </button>
      </section>
    </div>
  );
}