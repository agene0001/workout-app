import mysql.connector
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from sqlalchemy import create_engine
import gc
import h5py
import os
from scipy.sparse import save_npz, load_npz, csr_matrix
import tempfile

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MemoryEfficientRecommender:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.temp_dir = tempfile.mkdtemp()
        self.similarity_file = os.path.join(self.temp_dir, 'similarities.h5')

        try:
            logger.debug("Starting data loading process...")
            self.db = self._load_data_from_database()
            logger.info(f"Database loaded with {len(self.db)} rows")

            logger.debug("Starting initial setup...")
            self.setup('name', 'ingredients')
            logger.info("Initial setup completed successfully")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

    def _load_data_from_database(self):
        """Connect to MySQL and load the necessary data."""
        try:
            connection_str = f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
            engine = create_engine(connection_str)

            query = f"SELECT name, ingredients FROM {self.table_name}"
            logger.debug("Executing database query...")
            df = pd.read_sql(query, engine)

            logger.debug("Cleaning loaded data...")
            df['name'] = df['name'].fillna('')
            df['ingredients'] = df['ingredients'].fillna('')

            return df

        except Exception as err:
            logger.error(f"Database error: {err}")
            raise

    def _preprocess_text(self, text):
        """Preprocess text by cleaning and normalizing."""
        try:
            if not isinstance(text, str):
                return ""

            text = str(text).lower()
            text = re.sub(r'[^a-z0-9\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            return text

        except Exception as e:
            logger.error(f"Error in text preprocessing: {str(e)}")
            return ""

    def _calculate_batch_similarities(self, start_idx, end_idx):
        """Calculate similarities for a batch of items."""
        batch = self.tfidf_matrix[start_idx:end_idx]
        similarities = cosine_similarity(batch, self.tfidf_matrix)
        return similarities

    def setup(self, *args):
        """Prepare the data and generate the similarity matrix."""
        logger.debug("Starting setup process...")

        try:
            # Create query column
            logger.debug("Creating query column...")
            self.db['query'] = ''
            for arg in args:
                if arg in self.db.columns:
                    logger.debug(f"Processing column: {arg}")
                    self.db['query'] += self.db[arg].apply(self._preprocess_text) + ' '

            # Create TF-IDF matrix
            logger.debug("Creating TF-IDF vectorizer...")
            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=1000,  # Further reduced for memory efficiency
                max_df=0.95,
                min_df=2
            )

            logger.debug("Creating TF-IDF matrix...")
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.db['query'])

            # Save TF-IDF matrix to disk
            # tfidf_path = os.path.join(self.temp_dir, 'tfidf_matrix.npz')
            # save_npz(tfidf_path, self.tfidf_matrix)

            # Process similarities in smaller batches and save to HDF5
            batch_size = 500  # Smaller batch size
            n_samples = self.tfidf_matrix.shape[0]

            with h5py.File(self.similarity_file, 'w') as f:
                # Create dataset
                dset = f.create_dataset('similarities',
                                        shape=(n_samples, n_samples),
                                        dtype='f4',
                                        chunks=(batch_size, n_samples))

                for i in range(0, n_samples, batch_size):
                    end_idx = min(i + batch_size, n_samples)
                    logger.debug(f"Processing batch {i//batch_size + 1}/{(n_samples-1)//batch_size + 1}")

                    # Calculate similarities for this batch
                    batch_similarities = self._calculate_batch_similarities(i, end_idx)

                    # Save to HDF5 file
                    dset[i:end_idx, :] = batch_similarities

                    # Clear memory
                    del batch_similarities
                    gc.collect()

            logger.info("Setup completed successfully")

        except Exception as e:
            logger.error(f"Error during setup: {str(e)}")
            raise

    def find_ksimilar(self, title: str, k: int, titleCol: str = 'name'):
        """Find k similar items."""
        try:
            if not title or not isinstance(title, str):
                logger.error("Invalid title input")
                return pd.DataFrame()

            k = min(k, len(self.db) - 1)

            # Find the index of the query item
            matches = self.db[self.db[titleCol].str.lower() == title.lower()]
            if len(matches) == 0:
                logger.warning(f"No matches found for title: {title}")
                return pd.DataFrame()

            index = matches.index[0]

            # Read similarities from HDF5 file
            with h5py.File(self.similarity_file, 'r') as f:
                similarities = f['similarities'][index, :]

            # Get top k similar indices
            similar_indices = np.argsort(similarities)[::-1][1:k+1]

            # Return results
            result = self.db.iloc[similar_indices].copy()
            result['similarity_score'] = similarities[similar_indices]

            return result.sort_values('similarity_score', ascending=False)

        except Exception as e:
            logger.error(f"Error in find_ksimilar: {str(e)}")
            raise

    def __del__(self):
        """Cleanup temporary files."""
        try:
            if os.path.exists(self.similarity_file):
                os.remove(self.similarity_file)
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}")