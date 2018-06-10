import falcon


class Collection:
    """GET and POST instances of IT assets from/into an organization's IT service."""

    def on_get(self, req, resp, organization_code, it_service_instance_id):
        """ GETs a paged collection of IT assets in an organization IT service.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance.
        """
        pass

    def on_post(self, req, resp, organization_code, it_service_instance_id):
        """Adds an instance of IT asset to an organization IT service.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance.
        """
        pass


class Item:
    """GET, PATCH and DELETE an IT asset from an organization's IT service instance."""

    def on_patch(self, req, resp, organization_code, it_service_instance_id, it_asset_instance_id):
        """Updates (partially) the relationship IT service-IT asset requested.
        All entities that reference the relationship will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance to be patched.
        :param it_asset_instance_id: The id of the IT asset instance to be patched.
        """
        pass

    def on_delete(self, req, resp, organization_code, it_service_instance_id, it_asset_instance_id):
        """Removes an instance of IT asset from an organization IT service.
        It doesn't remove the IT asset from the organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance from which the IT asset should be removed.
        :param it_asset_instance_id: The id of the IT asset instance to be removed.
        """
        pass
