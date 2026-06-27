import { useEffect, useState } from 'react';
import { api } from '../api';

export default function PlaceExtras({ place }) {
  const [map, setMap] = useState(null);
  const [youtube, setYoutube] = useState(null);

  useEffect(() => {
    if (!place) return;
    api.map(place.latitude, place.longitude).then(setMap).catch(() => setMap(null));
    api.youtube(place.name).then(setYoutube).catch(() => setYoutube(null));
  }, [place]);

  if (!place) return null;

  return (
    <div className="place-extras">
      {map && (
        <div className="map-embed">
          <iframe
            title="Location map"
            src={map.embedUrl}
            loading="lazy"
            style={{ border: 0, width: '100%', height: '260px' }}
          />
          <a href={map.viewUrl} target="_blank" rel="noreferrer">Open larger map ↗</a>
        </div>
      )}
      {youtube && (
        <a className="youtube-link" href={youtube.searchUrl} target="_blank" rel="noreferrer">
          ▶ Watch travel videos for {place.name} on YouTube
        </a>
      )}
    </div>
  );
}
