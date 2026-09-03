import React from "react";
import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";

// Fake but plausible station coordinates for the demo corridor (Chennai suburban line)
const STATIONS = {
  A: [13.0827, 80.2707],
  B: [13.0500, 80.2200],
  C: [13.0200, 80.1700],
  D: [12.9900, 80.1200],
  E: [12.9600, 80.0700],
  F: [12.9300, 80.0200],
  G: [13.0000, 80.1950],
};

const RISK_COLOR = { critical: "#B33939", elevated: "#F4A300", low: "#2E7D32" };

export default function CorridorMap({ network, impact }) {
  const impactByCorridor = Object.fromEntries(impact.map((i) => [i.blocked_corridor, i]));

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="font-bold text-navy mb-1">Digital Twin — Corridor Network Impact</h2>
      <p className="text-sm text-gray-500 mb-4">
        Colour shows the risk of blocking that corridor today, based on whether diverted traffic overloads the alternate route.
      </p>
      <div style={{ height: 480 }} className="rounded-lg overflow-hidden">
        <MapContainer center={[13.0, 80.15]} zoom={11} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {network.edges.map((e) => {
            const info = impactByCorridor[e.corridor];
            const color = info ? RISK_COLOR[info.risk_level] || "#888" : "#888";
            return (
              <Polyline
                key={e.corridor}
                positions={[STATIONS[e.u], STATIONS[e.v]]}
                pathOptions={{ color, weight: 5 }}
              >
                <Popup>
                  <strong>{e.corridor}</strong> — {e.daily_trains} trains/day
                  <br />
                  {info ? info.verdict : "No block requested on this corridor."}
                </Popup>
              </Polyline>
            );
          })}
          {Object.entries(STATIONS).map(([name, pos]) => (
            <Marker key={name} position={pos}>
              <Popup>Station {name}</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
      <div className="flex gap-4 mt-3 text-xs">
        {Object.entries(RISK_COLOR).map(([label, color]) => (
          <span key={label} className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full inline-block" style={{ background: color }} />
            {label}
          </span>
        ))}
      </div>
    </div>
  );
}
