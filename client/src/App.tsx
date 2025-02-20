import React, { useState, useEffect } from 'react';
import { fetchPlayers, fetchPlayerDescription, PlayerStats } from './api';

const PlayerCard: React.FC<{ player: PlayerStats }> = ({ player }) => {
  const [description, setDescription] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showDescription, setShowDescription] = useState(false);

  const loadDescription = async () => {
    setIsLoading(true);
    try {
      const desc = await fetchPlayerDescription(player.player_name);
      setDescription(desc);
    } catch {
      setDescription(null);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    if (showDescription) {
      loadDescription();
    }
  }, [player.player_name, showDescription]);

  const formatNumber = (value: number | undefined): string => {
    return value !== undefined ? value.toFixed(3) : 'N/A';
  };

  const toggleDescription = () => {
    setShowDescription(!showDescription);
  };

  return (
    <div className="player-card">
      <div className="player-header">
        <h2 onClick={toggleDescription} style={{cursor: 'pointer'}}>{player.player_name}</h2>
        <button className="edit-button">Edit</button>
        <span className="position-tag">{player.position}</span>
      </div>

      <table className="player-stats-table">
        <thead>
          <tr>
            <th>Stat</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Games</td>
            <td>{player.games}</td>
          </tr>
          <tr>
            <td>At Bat</td>
            <td>{player.at_bat}</td>
          </tr>
          <tr>
            <td>Runs</td>
            <td>{player.runs}</td>
          </tr>
          <tr>
            <td>Hits</td>
            <td>{player.hits}</td>
          </tr>
          <tr>
            <td>Doubles</td>
            <td>{player.double_2b}</td>
          </tr>
          <tr>
            <td>3B</td>
            <td>{player.third_baseman}</td>
          </tr>
          <tr>
            <td>Home Runs</td>
            <td>{player.home_run}</td>
          </tr>
          <tr>
            <td>RBI</td>
            <td>{player.run_batted_in}</td>
          </tr>
          <tr>
            <td>Walks</td>
            <td>{player.a_walk}</td>
          </tr>
          <tr>
            <td>Strikeouts</td>
            <td>{player.strikeouts}</td>
          </tr>
          <tr>
            <td>Stolen Bases</td>
            <td>{player.stolen_base}</td>
          </tr>
          <tr>
            <td>Caught Stealing</td>
            <td>{player.caught_stealing}</td>
          </tr>
          <tr>
            <td>AVG</td>
            <td>{formatNumber(player.avg)}</td>
          </tr>
          <tr>
            <td>OBP</td>
            <td>{formatNumber(player.on_base_percentage)}</td>
          </tr>
          <tr>
            <td>SLG</td>
            <td>{formatNumber(player.slugging_percentage)}</td>
          </tr>
          <tr>
            <td>OPS</td>
            <td>{formatNumber(player.on_base_plus_slugging)}</td>
          </tr>
        </tbody>
      </table>

      {isLoading && showDescription ? (
        <div className="description-loading">Loading AI description...</div>
      ) : (
        showDescription && description && (
          <div className="player-description">
            <p>{description}</p>
          </div>
        )
      )}
    </div>
  );
};

const App: React.FC = () => {
  const [players, setPlayers] = useState<PlayerStats[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPlayers = async () => {
      try {
        setIsLoading(true);
        const data = await fetchPlayers(currentPage);
        setPlayers(data.players);
        setTotalPages(data.total_pages);
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to fetch players', error);
        setError('Unable to load players');
        setIsLoading(false);
      }
    };

    loadPlayers();
  }, [currentPage]);

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  if (isLoading) return <div>Loading players...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="app">
      <h1>Player Roster</h1>
      <div className="player-list">
        {players.map(player => (
          <PlayerCard key={player.player_name} player={player} />
        ))}
      </div>
      <div className="pagination">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
          <button
            key={page}
            onClick={() => handlePageChange(page)}
            className={page === currentPage ? 'active' : ''}
          >
            {page}
          </button>
        ))}
      </div>
    </div>
  );
};

export default App;