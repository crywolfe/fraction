import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface PlayerStats {
  player_name: string;
  position: string;
  games: number;
  at_bat: number;
  runs: number;
  hits: number;
  double_2b: number;
  third_baseman: number;
  home_run: number;
  run_batted_in: number;
  a_walk: number;
  strikeouts: number;
  stolen_base: number;
  caught_stealing: number;
  avg: number;
  on_base_percentage: number;
  slugging_percentage: number;
  on_base_plus_slugging: number;
}

export interface PlayerDescription {
  description: string;
}

export interface PlayersResponse {
  players: PlayerStats[];
  total_players: number;
  total_pages: number;
  current_page: number;
  page_size: number;
}

export const fetchPlayers = async (page = 1, pageSize = 10): Promise<PlayersResponse> => {
  try {
    console.log(`Fetching players - Page: ${page}, Page Size: ${pageSize}`);
    const response = await axios.get<PlayersResponse>(`${BASE_URL}/players`, {
      params: { 
        page: page, 
        page_size: pageSize 
      }
    });
    
    console.log('Players response:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('Failed to fetch players', error);
    throw error;
  }
};

export const fetchPlayerDescription = async (playerName: string): Promise<string> => {
  try {
    const response = await axios.get<PlayerDescription>(`${BASE_URL}/player/${playerName}/description`);
    return response.data.description;
  } catch (error) {
    console.error('Failed to fetch player description', error);
    return 'Description unavailable';
  }
};