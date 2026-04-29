import React from 'react';
import { DynamicTable } from './DynamicTable';
import { DynamicForm } from './DynamicForm';
import { DynamicCards } from './DynamicCards';
import { DynamicCharts } from './DynamicCharts';
import { DynamicCalendar } from './DynamicCalendar';

interface Props {
  components: string[];
  pageName: string;
}

export const DynamicRenderer: React.FC<Props> = ({ components, pageName }) => {
  return (
    <div className="space-y-8">
      {components.map((comp, idx) => {
        const type = comp.toLowerCase();
        if (type === 'cards') return <DynamicCards key={idx} pageName={pageName} />;
        if (type === 'charts') return <DynamicCharts key={idx} pageName={pageName} />;
        if (type === 'table') return <DynamicTable key={idx} pageName={pageName} />;
        if (type === 'form') return <DynamicForm key={idx} pageName={pageName} />;
        if (type === 'calendar') return <DynamicCalendar key={idx} />;
        
        return (
          <div key={idx} className="p-6 rounded-xl bg-white/5 border border-white/10 text-center text-gray-400">
            Unknown Component: {comp}
          </div>
        );
      })}
    </div>
  );
};