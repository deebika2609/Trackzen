import React, { useMemo } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const DEPT_COLORS = {
  Engineering: "#1F3B6E",
  "S&T": "#2E7D32",
  TRD: "#B33939",
};

function toToday(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  const d = new Date();
  d.setHours(h, m, 0, 0);
  return d;
}

export default function ScheduleCalendar({ schedule }) {
  const events = useMemo(
    () =>
      schedule.assignments.map((a) => ({
        title: `${a.department}: ${a.task} (${a.corridor})`,
        start: toToday(a.start_time),
        end: toToday(a.end_time),
        department: a.department,
      })),
    [schedule]
  );

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="font-bold text-navy mb-1">
        Safety-Constrained Schedule — OR-Tools CP-SAT ({schedule.status})
      </h2>
      <p className="text-sm text-gray-500 mb-4">
        No department is double-booked. Tasks sharing a corridor are pulled into overlapping windows automatically.
      </p>
      <div style={{ height: 550 }}>
        <Calendar
          localizer={localizer}
          events={events}
          defaultView="day"
          views={["day"]}
          step={15}
          timeslots={2}
          eventPropGetter={(event) => ({
            style: { backgroundColor: DEPT_COLORS[event.department] || "#555" },
          })}
        />
      </div>
    </div>
  );
}
