

export const DynamicTable = ({ pageName }: { pageName: string }) => {
  const lower = pageName.toLowerCase();
  let headers = ['Name', 'Email', 'Role', 'Status'];
  let rows = [
    { name: 'Alice Smith', email: 'alice@example.com', role: 'Admin', status: 'Active' },
    { name: 'Bob Jones', email: 'bob@example.com', role: 'User', status: 'Offline' },
    { name: 'Charlie Day', email: 'charlie@example.com', role: 'User', status: 'Active' },
  ];

  if (lower.includes('product')) {
    headers = ['Product Name', 'Category', 'Price', 'Stock'];
    rows = [
      { name: 'Premium Wireless Headphones', email: 'Electronics', role: '$299', status: 'In Stock' },
      { name: 'Mechanical Keyboard', email: 'Electronics', role: '$149', status: 'Low Stock' },
      { name: 'Ergonomic Chair', email: 'Furniture', role: '$499', status: 'Out of Stock' },
    ];
  } else if (lower.includes('student')) {
    headers = ['Student Name', 'Grade', 'GPA', 'Status'];
    rows = [
      { name: 'Emma Wilson', email: '10th', role: '3.8', status: 'Enrolled' },
      { name: 'Liam Garcia', email: '11th', role: '3.5', status: 'Enrolled' },
    ];
  }

  return (
    <div className="w-full bg-dark-800 border border-white/5 rounded-2xl shadow-lg overflow-hidden">
      <div className="p-6 border-b border-white/5 flex justify-between items-center">
        <h3 className="text-lg font-bold capitalize">{pageName} Data</h3>
        <div className="flex gap-2">
          <input type="text" placeholder="Search..." className="bg-dark-900 border border-white/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-accent-cyan text-white" />
          <button className="bg-accent-violet hover:bg-accent-cyan text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors">Export</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5">
              {headers.map((h, i) => (
                <th key={i} className="p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-white/5">{h}</th>
              ))}
              <th className="p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-white/5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="p-4 font-medium text-white">{r.name}</td>
                <td className="p-4 text-gray-300">{r.email}</td>
                <td className="p-4 text-gray-300">{r.role}</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                    r.status.includes('Active') || r.status.includes('In Stock') || r.status.includes('Enrolled') 
                    ? 'bg-green-500/20 text-green-400' 
                    : r.status.includes('Low') || r.status.includes('Offline') 
                    ? 'bg-yellow-500/20 text-yellow-400'
                    : 'bg-red-500/20 text-red-400'
                  }`}>
                    {r.status}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <button className="text-accent-cyan hover:text-white transition-colors text-sm font-medium">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};