import axiosClient from "./axiosClient";

import type { CreateCompanyPayload, CompanyResponse, CompanyUserPayload } from "../types/company";

export const superAdminAPI = {
  // CREATE COMPANY (with admin)
  createCompany: async (data: CreateCompanyPayload) => {
    const res = await axiosClient.post("/companies/create_company", data);
    return res.data;
  },

  // LIST ALL COMPANIES
  getCompanies: async (): Promise<CompanyResponse[]> => {
    const res = await axiosClient.get("/companies/");
    return res.data;
  },

  // GET SINGLE COMPANY
  getCompanyById: async (id: string): Promise<CompanyResponse> => {
    const res = await axiosClient.get(`/companies/${id}`);
    return res.data;
  },

  // DELETE COMPANY
  deleteCompany: async (id: string) => {
    const res = await axiosClient.delete(`/companies/${id}`);
    return res.data;
  },

  // CREATE COMPANY USER (admin/staff under company)
  createCompanyUser: async (data: CompanyUserPayload) => {
    const res = await axiosClient.post("/companies/company-user", data);
    return res.data;
  },
};
