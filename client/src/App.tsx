import React, { useState, useEffect, ChangeEvent } from 'react';
import { fetchPlayers, fetchPlayerDescription, PlayerStats } from './api';

const PlayerCard: React.FC<{ player: PlayerStats }> = ({ player }) => {
  const [description, setDescription] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showDescription, setShowDescription] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editPlayerData, setEditPlayerData] = useState<PlayerStats>({ ...player });

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

  const handleEditChange = (e: ChangeEvent<HTMLInputElement>, stat: string) => {
    setEditPlayerData({ ...editPlayerData, [stat]: parseFloat(e.target.value) });
  };

  const handleSave = () => {
    // Call the API to update the player data
    // updatePlayer(player.id, editPlayerData) // Assuming player has an 'id' property
    //   .then(() => {
    //     setIsEditing(false);
    //   })
    //   .catch(error => {
    //     console.error("Failed to update player", error);
    //   });
    setIsEditing(false); // For now, just disable editing
  };

  const handleCancel = () => {
    setEditPlayerData({ ...player }); // Reset to original values
    setIsEditing(false);
  };

  return (
    <div className="player-card">
      <div className="player-header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <h2 onClick={toggleDescription} style={{ marginRight: '10px' }}>{player.player_name}</h2>
          <button className="edit-button" onClick={() => {
            setIsEditing(true);
            setEditPlayerData({...player});
          }}>
            {isEditing ? 'Close' : 'Edit'}
          </button>
        </div>
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
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.games}
                  onChange={(e) => handleEditChange(e, 'games')}
                />
              ) : (
                player.games
              )}
            </td>
          </tr>
          <tr>
            <td>At Bat</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.at_bat}
                  onChange={(e) => handleEditChange(e, 'at_bat')}
                />
              ) : (
                player.at_bat
              )}
            </td>
          </tr>
          <tr>
            <td>Runs</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.runs}
                  onChange={(e) => handleEditChange(e, 'runs')}
                />
              ) : (
                player.runs
              )}
            </td>
          </tr>
          <tr>
            <td>Hits</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.hits}
                  onChange={(e) => handleEditChange(e, 'hits')}
                />
              ) : (
                player.hits
              )}
            </td>
          </tr>
          <tr>
            <td>Doubles</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.double_2b}
                  onChange={(e) => handleEditChange(e, 'double_2b')}
                />
              ) : (
                player.double_2b
              )}
            </td>
          </tr>
          <tr>
            <td>3B</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.third_baseman}
                  onChange={(e) => handleEditChange(e, 'third_baseman')}
                />
              ) : (
                player.third_baseman
              )}
            </td>
          </tr>
          <tr>
            <td>Home Runs</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.home_run}
                  onChange={(e) => handleEditChange(e, 'home_run')}
                />
              ) : (
                player.home_run
              )}
            </td>
          </tr>
          <tr>
            <td>RBI</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.run_batted_in}
                  onChange={(e) => handleEditChange(e, 'run_batted_in')}
                />
              ) : (
                player.run_batted_in
              )}
            </td>
          </tr>
          <tr>
            <td>Walks</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.a_walk}
                  onChange={(e) => handleEditChange(e, 'a_walk')}
                />
              ) : (
                player.a_walk
              )}
            </td>
          </tr>
          <tr>
            <td>Strikeouts</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.strikeouts}
                  onChange={(e) => handleEditChange(e, 'strikeouts')}
                />
              ) : (
                player.strikeouts
              )}
            </td>
          </tr>
          <tr>
            <td>Stolen Bases</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.stolen_base}
                  onChange={(e) => handleEditChange(e, 'stolen_base')}
                />
              ) : (
                player.stolen_base
              )}
            </td>
          </tr>
          <tr>
            <td>Caught Stealing</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.caught_stealing}
                  onChange={(e) => handleEditChange(e, 'caught_stealing')}
                />
              ) : (
                player.caught_stealing
              )}
            </td>
          </tr>
          <tr>
            <td>AVG</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.avg}
                  onChange={(e) => handleEditChange(e, 'avg')}
                />
              ) : (
                formatNumber(player.avg)
              )}
            </td>
          </tr>
          <tr>
            <td>OBP</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.on_base_percentage}
                  onChange={(e) => handleEditChange(e, 'on_base_percentage')}
                />
              ) : (
                formatNumber(player.on_base_percentage)
              )}
            </td>
          </tr>
          <tr>
            <td>SLG</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.slugging_percentage}
                  onChange={(e) => handleEditChange(e, 'slugging_percentage')}
                />
              ) : (
                formatNumber(player.slugging_percentage)
              )}
            </td>
          </tr>
          <tr>
            <td>OPS</td>
            <td>
              {isEditing ? (
                <input
                  type="number"
                  value={editPlayerData.on_base_plus_slugging}
                  onChange={(e) => handleEditChange(e, 'on_base_plus_slugging')}
                />
              ) : (
                formatNumber(player.on_base_plus_slugging)
              )}
            </td>
          </tr>
        </tbody>
      </table>
      {isEditing && (
        <div>
          <button onClick={handleSave}>Save</button>
          <button onClick={handleCancel}>Cancel</button>
        </div>
      )}
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