import { useEffect, useState } from "react";
import { superAdminAPI } from "../../../api/superAdmin";
import type { CompanyResponse, CreateCompanyPayload } from "../../../types/company";

const CompaniesList = () => {
  const [companies, setCompanies] = useState<CompanyResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newCompany, setNewCompany] = useState<CreateCompanyPayload>({
    company_data: { name: "", email: "", phone_number: "", address: "" },
    admin_data: { full_name: "", email: "", phone_number: "", password: "", role_name: "companyadmin", company_id: "" },
  });

  const loadCompanies = async () => {
    setLoading(true);
    try {
      const data = await superAdminAPI.getCompanies();
      setCompanies(data);
    } catch (error) {
      console.error("Failed to fetch companies:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCompanies();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this company?")) return;
    try {
      await superAdminAPI.deleteCompany(id);
      loadCompanies();
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreate = async () => {
    try {
      await superAdminAPI.createCompany(newCompany);
      setShowCreateForm(false);
      setNewCompany({
        company_data: { name: "", email: "", phone_number: "", address: "" },
        admin_data: { full_name: "", email: "", phone_number: "", password: "", role_name: "companyadmin", company_id: "" },
      });
      loadCompanies();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">Companies</h2>

      {/* Create Company Toggle */}
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4 hover:bg-blue-700"
        onClick={() => setShowCreateForm(!showCreateForm)}
      >
        {showCreateForm ? "Cancel" : "Create New Company"}
      </button>

      {/* Create Company Form */}
      {showCreateForm && (
        <div className="mb-6 p-4 border border-gray-300 rounded bg-gray-50">
          <h3 className="text-xl font-semibold mb-2">New Company</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
            <input
              type="text"
              placeholder="Company Name"
              value={newCompany.company_data.name}
              onChange={(e) => setNewCompany({ ...newCompany, company_data: { ...newCompany.company_data, name: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="email"
              placeholder="Company Email"
              value={newCompany.company_data.email}
              onChange={(e) => setNewCompany({ ...newCompany, company_data: { ...newCompany.company_data, email: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="text"
              placeholder="Company Phone"
              value={newCompany.company_data.phone_number}
              onChange={(e) => setNewCompany({ ...newCompany, company_data: { ...newCompany.company_data, phone_number: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="text"
              placeholder="Company Address"
              value={newCompany.company_data.address}
              onChange={(e) => setNewCompany({ ...newCompany, company_data: { ...newCompany.company_data, address: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
          </div>

          <h4 className="text-lg font-semibold mb-2">Admin Details</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
            <input
              type="text"
              placeholder="Admin Full Name"
              value={newCompany.admin_data.full_name}
              onChange={(e) => setNewCompany({ ...newCompany, admin_data: { ...newCompany.admin_data, full_name: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="email"
              placeholder="Admin Email"
              value={newCompany.admin_data.email}
              onChange={(e) => setNewCompany({ ...newCompany, admin_data: { ...newCompany.admin_data, email: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="text"
              placeholder="Admin Phone"
              value={newCompany.admin_data.phone_number}
              onChange={(e) => setNewCompany({ ...newCompany, admin_data: { ...newCompany.admin_data, phone_number: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
            <input
              type="password"
              placeholder="Admin Password"
              value={newCompany.admin_data.password}
              onChange={(e) => setNewCompany({ ...newCompany, admin_data: { ...newCompany.admin_data, password: e.target.value } })}
              className="p-2 border border-gray-300 rounded w-full"
            />
          </div>

          <button
            onClick={handleCreate}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Create
          </button>
        </div>
      )}

      {/* Companies Table */}
      {loading ? (
        <p>Loading...</p>
      ) : companies.length === 0 ? (
        <p>No companies found.</p>
      ) : (
        <table className="table-auto w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-300 px-4 py-2">Name</th>
              <th className="border border-gray-300 px-4 py-2">Email</th>
              <th className="border border-gray-300 px-4 py-2">Phone</th>
              <th className="border border-gray-300 px-4 py-2">Address</th>
              <th className="border border-gray-300 px-4 py-2">Created</th>
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {companies.map((company) => (
              <tr key={company.id} className="hover:bg-gray-100">
                <td className="border border-gray-300 px-4 py-2">{company.name}</td>
                <td className="border border-gray-300 px-4 py-2">{company.email}</td>
                <td className="border border-gray-300 px-4 py-2">{company.phone_number}</td>
                <td className="border border-gray-300 px-4 py-2">{company.address}</td>
                <td className="border border-gray-300 px-4 py-2">{new Date(company.created_at).toLocaleString()}</td>
                <td className="border border-gray-300 px-4 py-2 space-x-2">
                  <button
                    className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                    onClick={() => alert(`View ${company.name}`)}
                  >
                    View
                  </button>
                  <button
                    className="bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600"
                    onClick={() => alert(`Edit ${company.name}`)}
                  >
                    Edit
                  </button>
                  <button
                    className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                    onClick={() => handleDelete(company.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CompaniesList;
