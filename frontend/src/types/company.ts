
export interface CreateCompanyPayload {
  company_data: {
    name: string;
    email: string;
    phone_number: string;
    address: string;
  };
  admin_data: {
    full_name: string;
    email: string;
    phone_number: string;
    password: string;
    role_name: string;
    company_id: string;
  };
}

export interface CompanyUserPayload {
  full_name: string;
  email: string;
  phone_number: string;
  password: string;
  role_name: string;
  company_id: string;
}

export interface CompanyResponse {
  id: string;
  name: string;
  email: string;
  phone_number: string;
  address: string;
  created_at: string;
}