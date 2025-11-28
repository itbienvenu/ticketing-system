export interface RegisterUser {
  full_name: string;
  phone_number: string;
  email: string;
  password: string;
}

export interface LoginUser {
  email?: string;
  phone_number?: string;
  password_hash: string;
}

export interface UserOut {
  id: string;
  full_name: string;
  email: string;
  phone_number?: string;
  role?: string;
  roles?: string[];
}

export interface UpdateUser {
  full_name?: string;
  email?: string;
  phone_number?: string;
  role?: string;
}
