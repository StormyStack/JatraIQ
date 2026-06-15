import { Thermometer, Droplets, Wind, CloudRain } from "lucide-react";
import { CircularProgress } from "./CircularProgress";

export interface CitySnapshot {
  city: string;
  fetched_at: string;
  temp: number;
  feels_like: number;
  humidity: number;
  rain_probability: number;
  weather_main: string;
  wind_speed: number;
  aqi: number;
  pm2_5: number;
  overall_score: number;
  category: string;
}

interface CityCardProps {
  city: CitySnapshot;
  index: number;
}

function getCategoryStyles(category: string) {
  const c = category.toLowerCase();
  if (c.includes("excellent") || c.includes("good")) {
    return {
      badge:
        "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 ring-emerald-500/10",
      glow: "bg-emerald-500/10",
      ring: "#4ade80",
    };
  }
  if (c.includes("moderate")) {
    return {
      badge:
        "bg-amber-500/10 text-amber-400 border-amber-500/20 ring-amber-500/10",
      glow: "bg-amber-500/10",
      ring: "#facc15",
    };
  }
  return {
    badge:
      "bg-red-500/10 text-red-400 border-red-500/20 ring-red-500/10",
    glow: "bg-red-500/10",
    ring: "#f87171",
  };
}

export function CityCard({ city, index }: CityCardProps) {
  const styles = getCategoryStyles(city.category);

  return (
    <div
      className="group relative overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6 backdrop-blur-xl transition-all duration-500 hover:border-white/[0.12] hover:bg-white/[0.04]"
      style={{
        animation: `cardEnter 0.6s ease-out ${index * 0.08}s both`,
      }}
    >
      {/* Ambient glow */}
      <div
        className={`absolute -right-8 -top-8 h-28 w-28 rounded-full ${styles.glow} blur-3xl transition-opacity duration-500 group-hover:opacity-70`}
      />

      <div className="relative flex items-start justify-between">
        <div className="min-w-0">
          <h3 className="text-lg font-bold tracking-tight text-foreground">
            {city.city}
          </h3>
          <p className="mt-0.5 text-xs capitalize text-muted-foreground">
            {city.weather_main}
          </p>
        </div>

        <div className="flex flex-col items-center">
          <CircularProgress
            value={city.overall_score}
            size={64}
            strokeWidth={4}
            color={styles.ring}
          />
          <span className="mt-1 text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            {city.overall_score.toFixed(0)}/100
          </span>
        </div>
      </div>

      <div className="mt-4">
        <span
          className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold ring-1 ${styles.badge}`}
        >
          {city.category}
        </span>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="flex items-center gap-2 text-sm text-foreground/80">
          <Thermometer className="h-4 w-4 shrink-0 text-primary/70" />
          <span className="tabular-nums">{city.temp.toFixed(1)}°C</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-foreground/80">
          <Droplets className="h-4 w-4 shrink-0 text-primary/70" />
          <span className="tabular-nums">{city.humidity}%</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-foreground/80">
          <Wind className="h-4 w-4 shrink-0 text-primary/70" />
          <span className="tabular-nums">AQI {city.aqi}</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-foreground/80">
          <CloudRain className="h-4 w-4 shrink-0 text-primary/70" />
          <span className="tabular-nums">
            {(city.rain_probability * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      <div className="mt-4 border-t border-white/[0.04] pt-3">
        <div className="flex items-center justify-between text-xs text-muted-foreground/60">
          <span className="tabular-nums">PM2.5: {city.pm2_5.toFixed(1)}</span>
          <span className="tabular-nums">
            Wind: {city.wind_speed.toFixed(1)} m/s
          </span>
        </div>
      </div>
    </div>
  );
}
