import { createFileRoute } from "@tanstack/react-router";
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { MapPin, RefreshCw, AlertTriangle } from "lucide-react";
import { CityCard, type CitySnapshot } from "@/components/CityCard";

const API_BASE = "https://jatraiq-api.up.railway.app";

const snapshotQueryOptions = queryOptions({
  queryKey: ["snapshot"],
  queryFn: async () => {
    const res = await fetch(`${API_BASE}/api/v1/snapshot`);
    if (!res.ok) throw new Error(`Failed to fetch snapshot: ${res.status}`);
    return res.json() as Promise<CitySnapshot[]>;
  },
});

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      {
        title: "JatraIQ — Bangladesh Travel Readiness",
      },
      {
        name: "description",
        content:
          "Real-time travel readiness dashboard for Bangladesh cities. Weather, air quality, and travel scores.",
      },
      {
        property: "og:title",
        content: "JatraIQ — Bangladesh Travel Readiness",
      },
      {
        property: "og:description",
        content:
          "Real-time travel readiness dashboard for Bangladesh cities.",
      },
    ],
  }),
  loader: ({ context }) =>
    context.queryClient.ensureQueryData(snapshotQueryOptions),
  component: Index,
  errorComponent: SnapshotError,
  notFoundComponent: SnapshotNotFound,
});

function SnapshotError({ error }: { error: Error }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-4">
      <div className="flex flex-col items-center text-center">
        <AlertTriangle className="h-10 w-10 text-destructive" />
        <h1 className="mt-4 text-xl font-semibold text-foreground">
          Failed to load data
        </h1>
        <p className="mt-2 max-w-sm text-sm text-muted-foreground">
          {error.message || "Could not fetch city data. Please try again."}
        </p>
      </div>
    </div>
  );
}

function SnapshotNotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="text-center">
        <h1 className="text-xl font-semibold text-foreground">No data found</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          The snapshot API returned no cities.
        </p>
      </div>
    </div>
  );
}

function Index() {
  const { data: cities } = useSuspenseQuery(snapshotQueryOptions);
  const queryClient = useQueryClient();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastRefreshMsg, setLastRefreshMsg] = useState<string | null>(null);

  const refreshMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE}/api/v1/pipeline/run`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`Pipeline failed: ${res.status}`);
      return res.json() as Promise<{
        status: string;
        cities_fetched: number;
      }>;
    },
    onSuccess: (data) => {
      setLastRefreshMsg(
        `Updated ${data.cities_fetched} cities just now`
      );
      queryClient.invalidateQueries({ queryKey: ["snapshot"] });
    },
    onError: (err) => {
      setLastRefreshMsg(
        err instanceof Error ? err.message : "Refresh failed"
      );
    },
    onSettled: () => {
      setIsRefreshing(false);
    },
  });

  const handleRefresh = () => {
    setIsRefreshing(true);
    setLastRefreshMsg(null);
    refreshMutation.mutate();
  };

  const lastUpdated = cities[0]?.fetched_at ?? "Unknown";

  return (
    <div className="relative min-h-screen overflow-hidden bg-background">
      {/* Background ambient glow */}
      <div className="pointer-events-none absolute -top-40 left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-primary/[0.04] blur-[120px]" />
      <div className="pointer-events-none absolute bottom-0 right-0 h-[400px] w-[600px] rounded-full bg-primary/[0.02] blur-[100px]" />

      <div className="relative mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {/* Header */}
        <header
          className="mb-12"
          style={{ animation: "fadeIn 0.8s ease-out" }}
        >
          <div className="flex flex-col items-center gap-2 sm:flex-row sm:items-baseline sm:gap-3">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10">
                <MapPin className="h-5 w-5 text-primary" />
              </div>
              <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                JatraIQ
              </h1>
            </div>
            <span className="hidden text-muted-foreground sm:inline">
              /
            </span>
            <span className="text-lg font-medium text-muted-foreground">
              Bangladesh Travel Readiness
            </span>
          </div>
          <p className="mt-2 text-center text-sm text-muted-foreground/60 sm:text-left">
            Last updated: {lastUpdated}
            {lastRefreshMsg && (
              <span className="ml-2 text-primary">· {lastRefreshMsg}</span>
            )}
          </p>
        </header>

        {/* City Grid */}
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {cities.map((city, i) => (
            <CityCard key={city.city} city={city} index={i} />
          ))}
        </div>
      </div>

      {/* Floating Refresh Button */}
      <button
        onClick={handleRefresh}
        disabled={isRefreshing}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2.5 rounded-full bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground shadow-xl shadow-primary/20 transition-all hover:scale-105 hover:bg-primary/90 hover:shadow-primary/30 active:scale-95 disabled:scale-100 disabled:cursor-not-allowed disabled:opacity-60"
      >
        <RefreshCw
          className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`}
        />
        <span>{isRefreshing ? "Refreshing..." : "Refresh Data"}</span>
      </button>
    </div>
  );
}
