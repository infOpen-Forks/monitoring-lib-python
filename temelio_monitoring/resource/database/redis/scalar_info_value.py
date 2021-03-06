"""
This ressource check Redis scalar info values
"""


from nagiosplugin import CheckError
from nagiosplugin import Metric
from nagiosplugin import Resource

from redis import StrictRedis
from redis.exceptions import RedisError


class ScalarInfoValue(Resource):
    """
    This ressource get one value from redis information about connections
    """

    def __init__(self, **kwargs):
        """
        Initialize ressource attributes

        :param host: Redis server ip address or fqdn
        :param port: Redis server listening port
        :param password: Password of username authorized to view stats
        :param metric_name: Redis informations metric name
        :param section_name: Redis informations section name
        :type host: string
        :type port: int
        :type password: string
        :type metric_name: string
        :type section_name: string
        """

        # Arguments management
        self.database_id = kwargs.get('database_id', 0)
        self.host = kwargs.get('host', '127.0.0.1')
        self.metric_name = kwargs.get('metric_name', '')
        self.password = kwargs.get('password', '')
        self.port = kwargs.get('port', 6379)
        self.section_name = kwargs.get('section_name', 'default')

        self.redis_infos = {}


    def _get_hit_rate(self):
        """
        Calculate and return Redis hit rate

        :returns: Database hit rate
        :rtype: float
        """

        keyspace_hits = self.redis_infos['keyspace_hits']
        keyspace_misses = self.redis_infos['keyspace_misses']
        divisor = keyspace_hits + keyspace_misses

        if divisor == 0:
            return 0.0

        return float(keyspace_hits / (keyspace_hits + keyspace_misses))


    def probe(self):
        """
        Get information data about connections and return Metric objects

        :return: a generator with informations
        :rtype: generator
        """

        try:
            # Connect to redis server
            redis_client = StrictRedis(
                db=self.database_id,
                host=self.host,
                password=self.password,
                port=self.port)

            # Get statistics
            self.redis_infos = redis_client.info(section=self.section_name)
        except RedisError as error:
            raise CheckError(
                'Error with Redis server connection: {}'.format(str(error)))

        # Get metric value, or raise
        metric_value = None
        if self.metric_name == 'hit_rate':
            metric_value = self._get_hit_rate()
        elif self.metric_name in self.redis_infos:
            metric_value = self.redis_infos[self.metric_name]
        else:
            raise CheckError(
                '"{}": Unknown info metric name'.format(self.metric_name))


        # Build and return Metric objects from data if scalar, else raise
        if isinstance(metric_value, int) or isinstance(metric_value, float):
            yield Metric('db{}_{}'.format(self.database_id, self.metric_name),
                         metric_value)
        else:
            raise CheckError(
                '"{}" value is not an integer or float: "{}" !'.format(
                    self.metric_name, metric_value))
