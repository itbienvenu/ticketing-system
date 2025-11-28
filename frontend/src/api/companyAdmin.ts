import axiosClient from "./axiosClient";

export const getCompanyTickets = async () => {
  const { data } = await axiosClient.get("/company/tickets");
  return data;
};

export const assignTicket = async (ticketId: string, userId: string) => {
  const { data } = await axiosClient.post(`/tickets/${ticketId}/assign`, { userId });
  return data;
};
