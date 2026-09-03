import React from "react";

export default function AuctionPanel({ groups }) {
  const totalSaved = groups.reduce((sum, g) => sum + g.blocks_saved, 0);
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="font-bold text-navy mb-1">Auction Negotiation Engine</h2>
      <p className="text-sm text-gray-500 mb-4">
        Fairly combines multi-department requests that share a corridor into one block.{" "}
        <span className="font-semibold text-navy">{totalSaved} separate disruptions avoided</span> this cycle.
      </p>
      <div className="grid md:grid-cols-2 gap-3">
        {groups.map((g) => (
          <div
            key={g.corridor}
            className={`border rounded-lg p-3 ${g.blocks_saved > 0 ? "bg-amber/10 border-amber" : "bg-gray-50"}`}
          >
            <div className="flex justify-between items-center mb-1">
              <span className="font-semibold">Corridor {g.corridor}</span>
              <span className="text-xs bg-navy text-white px-2 py-0.5 rounded-full">
                {g.departments_combined.join(" + ")}
              </span>
            </div>
            <p className="text-sm text-gray-700">{g.reason}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
