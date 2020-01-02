# Datapunt-Django-Snapshot

Datapunt-Django-snapshot is a django app to help quickly scrape and process APIs.

Several datasources provide APIs or XML files that contain new data every x amount of minutes. 
This library was created as a generic way to save that data as a snapshot (raw, unprocessed) in the database and then proceed to process it in another table defining fields for the content.

## Structure:

All the following classes are supposed to be overriden with project specific parameters when the library is imported.

### Model
#### BaseSnapshot
The BaseSnapshot model contains `scraped_at` timestamp for the time the data was scraped and `data` JSONField for saving the data as is.

### Scraper

#### BaseAPIScraper
BaseAPIScraper is invoked with the `start` method. The class mainly does a `GET` request to fetch the data and creates a Snapshot model instance with the content added to the JSONField. 

It is possible to scrape an API that requires authentication by adding an `auth_url` attribute to the class and overriding the `authenticate` method. The authenticate method will run at the beginning if `auth_url` exists.

### Importers

####  BaseSnapshotImporter
BaseSnapshotImporter is invoked with the `start_import` method. The class imports one snapshot instance. Normally a snapshot instance contains a list of records that are unpacked and saved into a processed table. The class only loops through the list and uses the BaseImportFactory for creating the processed table instances. Finally, the class bulk saves the instances. 

Several methods in the BaseSnapshotImporter can be overriden for specific behviour. 


#### BaseImportFactory

BaseImportFactory class processes one raw record by mapping the record attributes to the processed table's fields. The class uses ModelForm to validate the record, which should be added to the class as an attribute.

For example a record can be like so:

```
{
    id: 1.
    location: 'Amsterdam',
    averageTemprature: 12
}
```

The processed table/model would be:

```
class TemperatureSensor(models.Model):
    api_id = models.IntegerField()
    city = models.CharField(max_length=30)
    average_temperature = models.IntegerField()
```

You would then define the mapping in the class:

```
self.raw_to_model_fields = {
    'id': 'api_id',
    'location': 'city',
    'averageTemparture', 'average_temperature'
}
```

### Manager

#### BaseSnapshotManager
 Used to add query iterator with limit-offset feature. This feature allows querying the whole table in batches without loading all the rows in memory.

## Code speaks louder than words

Go to https://github.com/Amsterdam/waarnemingen-boten to check a working example of how the library is used in a project.