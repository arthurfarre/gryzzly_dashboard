import React, { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Search, ChevronUp, ChevronDown } from 'lucide-react';

const Dashboard = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("margin"); // margin, revenue, cost
  const [sortDirection, setSortDirection] = useState("desc");
  const [tableSortField, setTableSortField] = useState("marginRate");
  const [tableSortDirection, setTableSortDirection] = useState("desc");
  
  // Données des projets
  const rawData = [
    {id: 1, project: "Valmy PRAEMIA", hours: 193.4, cost: 86945, revenue: 315000},
    {id: 2, project: "SNCF 1Pulsion (raynal)", hours: 281.3, cost: 122600, revenue: 256000},
    {id: 3, project: "SLB Béziers", hours: 53.9, cost: 24924, revenue: 225000},
    {id: 4, project: "Covivio Toulouse Bd Marquette", hours: 191.2, cost: 82257, revenue: 215382},
    {id: 5, project: "Accenture", hours: 200.3, cost: 81515, revenue: 160000},
    {id: 6, project: "Disney Hub Nord", hours: 89.8, cost: 35184, revenue: 130000},
    {id: 7, project: "Fondation Léonie Chaptal", hours: 85.1, cost: 41789, revenue: 100000},
    {id: 8, project: "Idemia Rennes", hours: 14.1, cost: 7749, revenue: 74000},
    {id: 9, project: "Astav Saint Armand", hours: 33.3, cost: 13469, revenue: 50000},
    {id: 10, project: "La poste - Saint Michel", hours: 33.0, cost: 14371, revenue: 49422},
    {id: 11, project: "Fogex Argenteuil", hours: 3.4, cost: 1998, revenue: 45000},
    {id: 12, project: "Newgen", hours: 109.3, cost: 54941, revenue: 40000},
    {id: 13, project: "Alten 2 - Campus Now", hours: 58.8, cost: 34780, revenue: 34000},
    {id: 14, project: "Algorithme Blagnac - projet paysager", hours: 9.8, cost: 4323, revenue: 30000},
    {id: 15, project: "Adoma Toulouse", hours: 42.6, cost: 21265, revenue: 28800},
    {id: 16, project: "Ossabois Vosges", hours: 16.8, cost: 8535, revenue: 28000},
    {id: 17, project: "Disney Merlin 2.2", hours: 17.8, cost: 7252, revenue: 27000},
    {id: 18, project: "Ossabois - extension Balbigny", hours: 14.1, cost: 8197, revenue: 25000},
    {id: 19, project: "Adam Boissons Mamirolle", hours: 34.4, cost: 17695, revenue: 20000},
    {id: 20, project: "La Palette Rouge - Agua", hours: 25.1, cost: 10231, revenue: 19700},
    {id: 21, project: "Hennessy Cognac", hours: 38.8, cost: 14389, revenue: 12000},
    {id: 22, project: "Rooj Gennevilliers Coeur des agnettes", hours: 2.6, cost: 1009, revenue: 12000},
    {id: 23, project: "Bureaux GA Paris", hours: 4.2, cost: 2602, revenue: 11650},
    {id: 24, project: "Hamelin", hours: 3.4, cost: 1117, revenue: 9125},
    {id: 25, project: "Limoges Fourche", hours: 2.3, cost: 828, revenue: 9000}
  ];

  // Calcul des données avec marges
  const processedData = useMemo(() => {
    return rawData.map(item => {
      const margin = item.revenue - item.cost;
      const marginRate = (item.revenue > 0 ? (margin / item.revenue) * 100 : 0).toFixed(1);
      // Conversion en k€
      const revenueK = (item.revenue / 1000).toFixed(1);
      const costK = (item.cost / 1000).toFixed(1);
      const marginK = (margin / 1000).toFixed(1);
      return {
        ...item,
        margin,
        marginRate: parseFloat(marginRate),
        revenueK: parseFloat(revenueK),
        costK: parseFloat(costK),
        marginK: parseFloat(marginK)
      };
    });
  }, [rawData]);

  // Fonction pour trier les données de tableau
  const handleTableSort = (field) => {
    if (tableSortField === field) {
      // Inverser la direction si on clique sur le même champ
      setTableSortDirection(tableSortDirection === "asc" ? "desc" : "asc");
    } else {
      // Nouveau champ, par défaut descendant
      setTableSortField(field);
      setTableSortDirection("desc");
    }
  };

  // Filtrage et tri des données pour le graphique
  const filteredAndSortedChartData = useMemo(() => {
    const filtered = processedData.filter(item => 
      item.project.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    const sorted = [...filtered].sort((a, b) => {
      const direction = sortDirection === "asc" ? 1 : -1;
      if (sortBy === "margin") return direction * (b.marginRate - a.marginRate);
      if (sortBy === "revenue") return direction * (b.revenue - a.revenue);
      if (sortBy === "cost") return direction * (b.cost - a.cost);
      return 0;
    });
    
    return sorted;
  }, [processedData, searchTerm, sortBy, sortDirection]);

  // Tri des données pour le tableau
  const sortedTableData = useMemo(() => {
    const filtered = processedData.filter(item => 
      item.project.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    return [...filtered].sort((a, b) => {
      const direction = tableSortDirection === "asc" ? 1 : -1;
      
      // Tri alphanumérique pour le nom du projet
      if (tableSortField === "project") {
        return direction * a.project.localeCompare(b.project);
      }
      
      // Tri numérique pour les autres champs
      return direction * (a[tableSortField] - b[tableSortField]);
    });
  }, [processedData, searchTerm, tableSortField, tableSortDirection]);

  // Calcul des statistiques globales
  const stats = useMemo(() => {
    const totalRevenue = processedData.reduce((sum, item) => sum + item.revenue, 0);
    const totalCost = processedData.reduce((sum, item) => sum + item.cost, 0);
    const totalMargin = totalRevenue - totalCost;
    const avgMarginRate = (totalMargin / totalRevenue * 100).toFixed(1);
    
    // Conversion en k€
    const totalRevenueK = (totalRevenue / 1000).toFixed(1);
    const totalCostK = (totalCost / 1000).toFixed(1);
    const totalMarginK = (totalMargin / 1000).toFixed(1);
    
    const highestMarginProject = [...processedData].sort((a, b) => b.marginRate - a.marginRate)[0];
    const lowestMarginProject = [...processedData].filter(p => p.revenue > 0).sort((a, b) => a.marginRate - b.marginRate)[0];
    
    return {
      totalRevenue,
      totalCost,
      totalMargin,
      totalRevenueK,
      totalCostK,
      totalMarginK,
      avgMarginRate,
      highestMarginProject,
      lowestMarginProject
    };
  }, [processedData]);

  // Fonction pour formater les montants en k€
  const formatKEuro = (amount) => {
    return `${amount.toFixed(1)} k€`;
  };

  // Fonction pour déterminer la couleur en fonction du taux de marge
  const getMarginColor = (marginRate) => {
    if (marginRate >= 70) return "#4CAF50"; // Vert
    if (marginRate >= 50) return "#8BC34A"; // Vert-jaune
    if (marginRate >= 30) return "#CDDC39"; // Jaune-vert
    if (marginRate >= 10) return "#FFC107"; // Jaune-orange
    return "#F44336"; // Rouge
  };

  // Composant pour l'en-tête de colonne triable
  const SortableHeader = ({ field, label, alignment = "left" }) => {
    const isSorted = tableSortField === field;
    const SortIcon = isSorted && tableSortDirection === "asc" ? ChevronUp : ChevronDown;
    
    return (
      <th 
        className={`px-6 py-3 text-${alignment} text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100`}
        onClick={() => handleTableSort(field)}
      >
        <div className="flex items-center justify-between">
          <span>{label}</span>
          {isSorted && <SortIcon size={14} />}
        </div>
      </th>
    );
  };

  return (
    <div className="flex flex-col p-6 bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard des Projets</h1>
        
        <div className="flex items-center">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Rechercher un projet..."
              className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select 
            className="ml-4 py-2 px-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="margin">Trier par marge (%)</option>
            <option value="revenue">Trier par revenus</option>
            <option value="cost">Trier par coûts</option>
          </select>
          
          <select 
            className="ml-4 py-2 px-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={sortDirection}
            onChange={(e) => setSortDirection(e.target.value)}
          >
            <option value="desc">Décroissant</option>
            <option value="asc">Croissant</option>
          </select>
        </div>
      </div>
      
      {/* Cards statistiques */}
      <div className="grid grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm text-gray-500 mb-1">Revenus Totaux</h3>
          <p className="text-2xl font-bold">{formatKEuro(parseFloat(stats.totalRevenueK))}</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm text-gray-500 mb-1">Coûts Totaux</h3>
          <p className="text-2xl font-bold">{formatKEuro(parseFloat(stats.totalCostK))}</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm text-gray-500 mb-1">Marge Totale</h3>
          <p className="text-2xl font-bold">{formatKEuro(parseFloat(stats.totalMarginK))}</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm text-gray-500 mb-1">Taux de Marge Moyen</h3>
          <p className="text-2xl font-bold">{stats.avgMarginRate}%</p>
        </div>
      </div>
      
      {/* Graphique principal */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Taux de Marge par Projet</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={filteredAndSortedChartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 120 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="project" 
                angle={-45} 
                textAnchor="end" 
                height={120} 
                interval={0}
              />
              <YAxis 
                label={{ value: 'Taux de Marge (%)', angle: -90, position: 'insideLeft' }}
                domain={[0, 100]}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === "marginRate") return [`${value}%`, "Taux de Marge"];
                  if (name === "revenueK") return [`${value} k€`, "Revenus"];
                  if (name === "costK") return [`${value} k€`, "Coûts"];
                  if (name === "marginK") return [`${value} k€`, "Marge"];
                  return [value, name];
                }}
                labelFormatter={(value) => `Projet: ${value}`}
              />
              <Legend />
              <Bar dataKey="marginRate" name="Taux de Marge (%)" radius={[4, 4, 0, 0]}>
                {filteredAndSortedChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getMarginColor(entry.marginRate)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Tableau de données */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <SortableHeader field="project" label="Projet" />
              <SortableHeader field="hours" label="Heures" alignment="right" />
              <SortableHeader field="costK" label="Coûts (k€)" alignment="right" />
              <SortableHeader field="revenueK" label="Revenus (k€)" alignment="right" />
              <SortableHeader field="marginK" label="Marge (k€)" alignment="right" />
              <SortableHeader field="marginRate" label="Taux de Marge" alignment="right" />
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedTableData.map((project) => (
              <tr key={project.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{project.project}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{project.hours.toLocaleString('fr-FR')}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{formatKEuro(project.costK)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{formatKEuro(project.revenueK)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{formatKEuro(project.marginK)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <span 
                    className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full"
                    style={{ backgroundColor: `${getMarginColor(project.marginRate)}20`, color: getMarginColor(project.marginRate) }}
                  >
                    {project.marginRate}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
